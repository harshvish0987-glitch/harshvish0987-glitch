# Smart AI Chatbot

A Flask-based conversational AI application integrating the Google Gemini API with a browser-based chat interface and document text extraction.

## Purpose

The project explores a lightweight AI assistant architecture in which a Flask backend receives user messages, sends them to a Gemini model, and returns generated responses to a web client. It also includes an upload workflow for extracting text from supported documents.

## Current Implementation

The current source contains:

- Flask routes for the landing page and chat page.
- A `/ask` API endpoint for sending user messages to Gemini.
- Gemini integration using the `google-genai` Python package.
- PDF text extraction using PyPDF2.
- DOCX text extraction using python-docx.
- A browser UI implemented with HTML, CSS, and JavaScript.
- Static client-side utilities for chat UI and browser storage.
- Gunicorn configuration through a Procfile for deployment-oriented execution.

## How It Works

1. A user opens the web chat interface.
2. The frontend sends a message to the Flask `/ask` endpoint.
3. Flask validates the message and creates a Gemini client using the `GEMINI_API_KEY` environment variable.
4. The backend sends the message to the configured Gemini model.
5. The generated response is returned to the browser as JSON.
6. Uploaded PDF or DOCX files are parsed on the server and their extracted text is returned to the client.

## Supported File Inputs

- PDF
- DOCX

Other file types are rejected by the current upload endpoint.

## Technology

- Python
- Flask
- Google Gemini API
- google-genai
- PyPDF2
- python-docx
- Gunicorn
- HTML5
- CSS3
- JavaScript

## Results

The current implementation demonstrates the core chat request/response flow and server-side PDF/DOCX text extraction. It is not yet a complete production chatbot platform.

## Configuration

Set the Gemini API key through an environment variable:

```bash
GEMINI_API_KEY="your-api-key"
```

Do not place API credentials directly in source code or commit them to GitHub.

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Set `GEMINI_API_KEY`, then run:

```bash
python app.py
```

For a production-style process, the included Procfile uses Gunicorn.

## Status

In Development. The current implementation is functional at the core chat and document-extraction level, but the overall application is not yet presented as a completed production system.

## Planned Improvements

- Stronger conversation-state handling.
- More complete document-aware prompting.
- Improved validation and error handling.
- Persistent user data and authentication.
- Production configuration and deployment hardening.
- Broader automated and manual testing coverage.
