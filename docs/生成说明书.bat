@echo off
rem ============================================================
rem  Rebuild the manual and re-inject it into index.html.
rem
rem  Source of truth:  docs\<the manual>.md
rem  Outputs:          the HTML manual, help.html, and the embedded copy
rem
rem  Requires Python 3 (standard library only, no pip installs).
rem  This file is deliberately ASCII-only and CRLF: no codepage issues.
rem ============================================================
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo.
  echo   [!] Python 3 not found.
  echo       Get it from https://www.python.org/downloads/
  echo       and tick "Add python.exe to PATH" during install.
  echo.
  pause
  exit /b 1
)

echo.
echo   Rebuilding manual from the markdown source ...
echo.
%PY% build_help.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo   [OK] Done. Open the HTML manual in the parent folder to check.
) else (
  echo   [FAIL] build_help.py exited with code %RC%
)
echo.
pause
exit /b %RC%
