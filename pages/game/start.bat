@echo off
setlocal

cd /d "%~dp0"

set "PORT=5000"
set "URL=http://localhost:%PORT%"

where python >nul 2>nul
if %errorlevel%==0 goto run_python

where py >nul 2>nul
if %errorlevel%==0 goto run_py

echo [Error] Python not found.
echo Please install Python 3, then run this file again.
pause
exit /b 1

:run_python
start "" "%URL%"
echo Starting server at %URL%
python -m http.server %PORT%
goto end

:run_py
start "" "%URL%"
echo Starting server at %URL%
py -m http.server %PORT%

:end
endlocal
