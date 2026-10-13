@echo off
rem ============================================================
rem  DaoYing / Dynamic Island Gradient - Windows launcher
rem  Just opens index.html in your default browser.
rem  (This file is ASCII-only on purpose: no codepage issues.)
rem ============================================================
cd /d "%~dp0"

if not exist "index.html" (
  echo.
  echo   [!] index.html not found next to this launcher.
  echo       Please keep the two files in the same folder.
  echo.
  pause
  exit /b 1
)

rem Open with the default browser
start "" "index.html"

echo.
echo   DaoYing is opening in your browser...
echo   If nothing happens, just double-click index.html instead.
echo.
timeout /t 3 >nul
exit /b 0
