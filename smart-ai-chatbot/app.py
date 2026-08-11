from flask import Flask, render_template, request, jsonify
from google import genai
from PyPDF2 import PdfReader
from docx import Document
from config import GEMINI_API_KEY

app = Flask(__name__)


def get_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY environment variable is not configured")
    return genai.Client(api_key=GEMINI_API_KEY)


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        client = get_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_message,
        )

        return jsonify({"response": response.text})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/upload-file", methods=["POST"])
def upload_file():
    try:
        file = request.files.get("file")

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        filename = file.filename.lower()
        extracted_text = ""

        if filename.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                extracted_text += page.extract_text() or ""

        elif filename.endswith(".docx"):
            document = Document(file)
            for para in document.paragraphs:
                extracted_text += para.text + "\n"

        else:
            return jsonify({"error": "Unsupported file type"}), 400

        return jsonify({"content": extracted_text})

    except Exception as e:
        print("UPLOAD ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
