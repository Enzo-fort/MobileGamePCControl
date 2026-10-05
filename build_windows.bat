@echo off
setlocal
cd /d "%~dp0"
py -m pip install -r requirements.txt pyinstaller
py -m PyInstaller --noconfirm --clean --onefile --windowed --name MobileGamePCControl main.py
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b 1
)
echo.
echo Built: dist\MobileGamePCControl.exe
echo.
pause
