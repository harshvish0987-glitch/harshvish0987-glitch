@echo off
setlocal
if "%GEMINI_API_KEY%"=="" (
  echo Set GEMINI_API_KEY in your environment before starting.
  echo Example: set GEMINI_API_KEY=YOUR_KEY
  exit /b 1
)
python -m pip install -r requirements.txt
start "Smart Resume Analyzer API" cmd /k "python api\index.py"
npm install
npm run dev
