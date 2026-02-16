@echo off
echo ============================================
echo  RC Investment Properties - Local Server
echo ============================================
echo.
echo Starting local server at http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo Opening browser...
start http://localhost:8000
echo.
python -m http.server 8000
pause
