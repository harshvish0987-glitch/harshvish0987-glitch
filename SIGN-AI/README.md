# SIGN-AI

A web-based sign language translation application that combines browser-based hand tracking with a Flask backend for gesture metadata, authentication, translation, history, and administrative logging.

## Purpose

SIGN-AI is designed to make hand-sign recognition accessible through a browser camera workflow. The frontend uses MediaPipe Hands to track hand landmarks and identify supported signs, while the Flask backend provides the application APIs and persistent application data.

## Current Implementation

The current source contains:

- Browser camera integration using MediaPipe Hands and MediaPipe Camera Utils.
- A gesture catalog containing 23 custom gestures, 26 alphabet entries, and 10 number entries.
- Flask API endpoints for health checks, gesture metadata, translation, authentication, translation history, and administrator logs.
- JWT-based authentication with password hashing.
- SQLAlchemy-backed persistence for users, session events, and translation history.
- Separate frontend pages for the landing page, translator, dashboard, history, settings, and administration.
- CORS support for the Flask API.

## How It Works

1. The browser requests camera access through the standard browser media API.
2. MediaPipe Hands processes the camera stream and provides hand-tracking data in the frontend.
3. The frontend identifies a supported sign and sends the corresponding gesture key to the Flask API.
4. The backend resolves the gesture metadata and returns the translated label.
5. Translation events can be stored with confidence and hand-count information for authenticated users.
6. Authenticated users can retrieve their translation history, while administrator accounts can access application log summaries.

## Backend API

Key endpoints include:

- `GET /api/health` — application health and gesture-count information.
- `GET /api/gestures` — supported gesture metadata with optional category filtering.
- `POST /api/register` — create a user account.
- `POST /api/login` — authenticate a user and issue a JWT.
- `POST /api/logout` — record a logout event.
- `POST /api/translate` — translate a supported gesture key.
- `POST /api/translation/log` — store a translation event.
- `GET /api/translations/history` — retrieve authenticated-user translation history.
- `GET /api/admin/logs` — retrieve administrator-only application summaries and logs.

## Technology

- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PyJWT
- HTML5
- CSS3
- JavaScript
- MediaPipe Hands

## Results

The implemented application provides a browser-based translation workflow with authentication, gesture metadata, translation responses, history logging, and administrator monitoring endpoints. The source does not establish a validated production accuracy percentage, so no accuracy claim is made here.

## Status

Source implementation available. This repository is not presented as a live production deployment.

## Security Notes

Secrets and local database files should not be committed. Configure `SIGNAI_SECRET_KEY` and `DATABASE_URL` through environment variables for deployment.
