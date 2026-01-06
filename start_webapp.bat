@echo off
cd /d "%~dp0"
echo Starting Pattern Recognition Web Application...
echo.
echo The web app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.
python -m streamlit run pattern_recognition_webapp.py
pause

