@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo Interactive SoC Clock Distribution Playbook
echo ============================================================

if not exist ".venv\Scripts\activate.bat" (
    echo Creating local Python virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        exit /b 1
    )

    call .venv\Scripts\activate.bat

    echo Upgrading pip...
    python -m pip install --upgrade pip

    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements.
        exit /b 1
    )
) else (
    call .venv\Scripts\activate.bat
)

echo.
echo Launching Streamlit app...
streamlit run app.py

endlocal