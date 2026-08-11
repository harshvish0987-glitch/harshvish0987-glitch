#!/usr/bin/env bash
set -e
: "${GEMINI_API_KEY:?Set GEMINI_API_KEY before starting}"
python3 -m pip install -r requirements.txt
python3 api/index.py &
npm install
npm run dev
