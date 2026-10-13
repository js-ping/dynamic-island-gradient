@echo off
rem ============================================================
rem  Build the "full" single file: index.html + the bundled HEIC decoder.
rem
rem  Source:   index.html            (clean source, MIT only, ~70 KB)
rem           tools\vendor\...      (libheif wasm, LGPL-3.0)
rem  Output:   dist\Daoying-full-heic.html   (~2 MB, what users download)
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
echo   Packing the full build (index.html + HEIC decoder) ...
echo.
%PY% build_full.py
set "RC=%ERRORLEVEL%"

echo.
if "%RC%"=="0" (
  echo   [OK] Done. The result is in ..\dist\
) else (
  echo   [FAIL] build_full.py exited with code %RC%
)
echo.
pause
exit /b %RC%
