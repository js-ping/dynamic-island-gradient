@echo off
rem ============================================================
rem  DaoYing / Dynamic Island Gradient - Windows launcher
rem  Finds the main program and opens it in your default browser.
rem
rem  The main program is picked automatically: index.html if present,
rem  otherwise the largest .html in this folder (the manual is ~27 KB,
rem  the app is 74 KB or 2.1 MB - so "largest" is always the app).
rem  That also keeps this file free of non-ASCII characters.
rem
rem  (This file is ASCII-only and CRLF on purpose: no codepage issues.)
rem ============================================================
cd /d "%~dp0"

set "TARGET="
if exist "index.html" set "TARGET=index.html"

if not defined TARGET (
  for /f "delims=" %%F in ('dir /b /o-s *.html 2^>nul') do (
    if not defined TARGET set "TARGET=%%F"
  )
)

if not defined TARGET (
  echo.
  echo   [!] No .html file found next to this launcher.
  echo       Please keep the launcher and the app in the same folder.
  echo.
  pause
  exit /b 1
)

echo.
echo   Opening: %TARGET%
start "" "%TARGET%"

echo.
echo   If nothing happens, just double-click %TARGET% instead.
echo.
timeout /t 3 >nul
exit /b 0
