# Smart Resume Analyzer & ATS Checker

An AI-assisted resume analysis platform for evaluating resume structure, ATS alignment, technical evidence, recruiter-facing green flags, red flags, and actionable improvements.

## Purpose

The application combines deterministic resume checks with Gemini structured analysis. The deterministic layer provides an explainable baseline score; Gemini adds contextual review when a server-side API key is configured.

## Core workflow

1. Upload a PDF, DOCX, or TXT resume.
2. Extract readable resume text on the Flask backend.
3. Calculate baseline structure, completeness, technical specificity, testing evidence, and keyword-alignment signals.
4. Optionally compare the resume against a target job description.
5. Send the resume and role context to Gemini using structured JSON output.
6. Combine the deterministic score with a constrained AI adjustment.
7. Display score, role fit, green flags, red flags, ATS terms, and recommendations.
8. Persist the analysis to SQLite locally and optionally to Firebase Firestore when Firebase credentials are configured.
9. Print the result as a PDF through the browser's print dialog.

## Technology

- Python
- Flask
- Next.js / React
- JavaScript / TypeScript
- HTML5 / CSS3
- Gemini API
- Firebase Firestore (optional persistence)
- SQLite / SQL
- REST endpoints

## API

`GET /api/health` checks backend availability and whether Gemini/Firebase environment variables are configured.

`POST /api/analyze` accepts multipart form data:

- `resume`: PDF, DOCX, or TXT file
- `job_description`: optional job description
- `target_role`: target role name

## Environment

The application reads Gemini and optional Firebase credentials from server-side environment variables. Do not create or commit an environment file containing credentials to the public repository.

For local development, configure `GEMINI_API_KEY` in your operating-system environment or your local development environment. Keep all secrets outside Git.

Never commit API keys, Firebase service-account credentials, database files, or `.env` files.

## Local development

Install frontend dependencies:

```bash
npm install
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask API:

```bash
python api/index.py
```

Run the Next.js application:

```bash
npm run dev
```

## Scoring philosophy

The displayed score is a resume-quality and job-alignment score, not a hiring probability. The baseline considers contact and identity, education, projects, skills, testing evidence, action-oriented writing, measurable evidence, and ATS readability. When a job description is supplied, keyword overlap becomes a major component. Gemini can adjust the baseline within a small bounded range after reviewing the actual text.

## Security

- Gemini credentials are read only from environment variables.
- Uploaded documents are processed in memory where possible.
- Local SQLite persistence is intended for local development or ephemeral server environments.
- Firebase persistence is optional and requires server-side credentials.
- No API key is included in the source distribution.
