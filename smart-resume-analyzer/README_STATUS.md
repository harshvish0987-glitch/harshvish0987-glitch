Status: Development project

The Smart Resume Analyzer & ATS Checker is implemented as a Next.js/React frontend with a Flask/Python analysis API. It supports PDF, DOCX and TXT extraction, deterministic ATS scoring, optional job-description matching, structured Gemini review, green flags, red flags, recommendations, SQLite persistence and optional Firebase Firestore persistence.

Configure GEMINI_API_KEY through the environment before using AI enhancement. Do not commit API keys, service-account credentials, resumes or database files.

Do not describe this project as production-ready until it has been deployed and externally tested with a configured Gemini API key.