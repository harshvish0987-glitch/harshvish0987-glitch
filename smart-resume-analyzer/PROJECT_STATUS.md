# Project Status

Status: Development project

This repository contains the Smart Resume Analyzer & ATS Checker implementation. It is intended to analyze uploaded resumes, produce an explainable baseline score, optionally compare the resume with a target job description, and use Gemini for structured contextual review.

The project should not be described as a production service until it has been deployed and externally tested with a configured Gemini API key.

## Current implementation

- PDF, DOCX, and TXT extraction
- Deterministic ATS and resume-quality scoring
- Optional job-description keyword matching
- Gemini structured analysis with bounded score adjustment
- Green flags and red flags
- Actionable recommendations
- SQLite persistence for local use
- Optional Firebase Firestore persistence
- Responsive Next.js interface
- Browser print-to-PDF report

## Security requirements

Configure `GEMINI_API_KEY` through an environment variable. Never commit the real key, Firebase service-account credentials, uploaded resumes, or local database files.
