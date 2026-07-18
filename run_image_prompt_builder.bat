@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_CMD="

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_CMD="%~dp0.venv\Scripts\python.exe""
) else (
    where py >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python was not found.
    echo Install Python 3, then run this file again.
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import PySide6" >nul 2>nul
if errorlevel 1 (
    echo PySide6 is not installed for the selected Python.
    echo Installing requirements...
    %PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo.
        echo Could not install requirements.
        pause
        exit /b 1
    )
)

%PYTHON_CMD% "%~dp0image_prompt_builder.py"
if errorlevel 1 (
    echo.
    echo Image Prompt Builder exited with an error.
    pause
    exit /b 1
)
