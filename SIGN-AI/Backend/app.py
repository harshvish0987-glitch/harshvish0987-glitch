import os
import datetime
from typing import Optional

import jwt
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from gestures import ALL_GESTURES, translate_key, get_gesture

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "signai.db")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "Frontend"),
    static_folder=os.path.join(BASE_DIR, "..", "Frontend"),
    static_url_path="",
)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SIGNAI_SECRET_KEY", "development-only-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///signai.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class SessionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    email = db.Column(db.String(255))
    action = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class TranslationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    email = db.Column(db.String(255))
    gesture_key = db.Column(db.String(64), nullable=False)
    gesture_label = db.Column(db.String(128))
    translation = db.Column(db.String(256))
    confidence = db.Column(db.Float)
    hand_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


def _current_user_from_token() -> Optional[User]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except Exception:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return User.query.get(user_id)


def _log_session_event(action: str, user: Optional[User]):
    try:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        ua = (request.headers.get("User-Agent") or "")[:255]
        entry = SessionLog(
            user_id=user.id if user else None,
            email=user.email if user else None,
            action=action,
            ip=ip,
            user_agent=ua,
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/translator")
def translator():
    return render_template("translator.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/history")
def history_page():
    return render_template("history.html")


@app.route("/settings")
def settings_page():
    return render_template("settings.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "ok",
        "gestures": len(ALL_GESTURES),
        "timestamp": datetime.datetime.utcnow().isoformat(),
    })


@app.route("/api/gestures")
def api_gestures():
    category = request.args.get("category")
    items = ALL_GESTURES
    if category == "gesture":
        items = [g for g in ALL_GESTURES if g["type"] in ("GESTURE", "2HAND")]
    elif category == "asl":
        items = [g for g in ALL_GESTURES if g["type"] == "ASL"]
    elif category == "num":
        items = [g for g in ALL_GESTURES if g["type"] == "NUM"]
    return jsonify({"gestures": items, "total": len(items)})


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        is_admin=User.query.count() == 0,
    )
    db.session.add(user)
    db.session.commit()
    _log_session_event("register", user)

    token = jwt.encode(
        {
            "sub": user.id,
            "email": user.email,
            "admin": user.is_admin,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    return jsonify({
        "message": "User registered successfully",
        "token": token,
        "name": user.name,
        "is_admin": user.is_admin,
    }), 200


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "sub": user.id,
            "email": user.email,
            "admin": user.is_admin,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8),
        },
        app.config["SECRET_KEY"],
        algorithm="HS256",
    )
    _log_session_event("login", user)
    return jsonify({"token": token, "name": user.name, "is_admin": user.is_admin})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    user = _current_user_from_token()
    if user:
        _log_session_event("logout", user)
    return jsonify({"message": "Logged out"}), 200


@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.json or {}
    gesture = data.get("gesture") or data.get("key")
    if not gesture:
        return jsonify({"error": "Gesture key is required"}), 400

    key = str(gesture).strip()
    meta = get_gesture(key)
    text = translate_key(key)

    return jsonify({
        "key": key,
        "translation": text,
        "label": meta["label"] if meta else text,
        "type": meta["type"] if meta else "UNKNOWN",
        "instruction": meta["instr"] if meta else "",
    })


@app.route("/api/translation/log", methods=["POST"])
def log_translation():
    data = request.json or {}
    key = data.get("gesture") or data.get("key")
    if not key:
        return jsonify({"error": "Gesture key is required"}), 400

    user = _current_user_from_token()
    meta = get_gesture(key)
    text = translate_key(key)
    conf = float(data.get("confidence") or 0)
    hands = int(data.get("hand_count") or 1)

    try:
        entry = TranslationLog(
            user_id=user.id if user else None,
            email=user.email if user else data.get("email"),
            gesture_key=key,
            gesture_label=meta["label"] if meta else key,
            translation=text,
            confidence=conf,
            hand_count=hands,
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to log translation"}), 500

    return jsonify({"message": "Logged", "translation": text})


@app.route("/api/translations/history", methods=["GET"])
def translation_history():
    user = _current_user_from_token()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    limit = min(int(request.args.get("limit", 50)), 200)
    logs = (
        TranslationLog.query.filter_by(user_id=user.id)
        .order_by(TranslationLog.created_at.desc())
        .limit(limit)
        .all()
    )
    return jsonify({
        "history": [
            {
                "id": log.id,
                "gesture_key": log.gesture_key,
                "gesture_label": log.gesture_label,
                "translation": log.translation,
                "confidence": log.confidence,
                "hand_count": log.hand_count,
                "timestamp": log.created_at.isoformat(),
            }
            for log in logs
        ]
    })


@app.route("/api/admin/logs", methods=["GET"])
def api_admin_logs():
    admin_user = _current_user_from_token()
    if not admin_user or not admin_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    today = datetime.date.today()
    today_start = datetime.datetime.combine(today, datetime.time.min)

    logs = SessionLog.query.order_by(SessionLog.created_at.desc()).limit(200).all()
    trans_count = TranslationLog.query.count()
    today_trans = TranslationLog.query.filter(TranslationLog.created_at >= today_start).count()

    return jsonify({
        "summary": {
            "total_users": User.query.count(),
            "total_admins": User.query.filter_by(is_admin=True).count(),
            "today_registrations": User.query.filter(User.created_at >= today_start).count(),
            "total_translations": trans_count,
            "today_translations": today_trans,
        },
        "logs": [
            {
                "id": log.id,
                "email": log.email,
                "action": log.action,
                "ip": log.ip,
                "user_agent": log.user_agent,
                "timestamp": log.created_at.isoformat(),
            }
            for log in logs
        ],
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, host="0.0.0.0", port=port)
