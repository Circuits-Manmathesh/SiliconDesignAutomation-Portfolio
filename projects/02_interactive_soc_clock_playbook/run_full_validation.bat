@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo Interactive SoC Clock Distribution Playbook - Full Validation
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
echo [1/4] Running final project audit...
python tools\final_project_audit.py
if errorlevel 1 exit /b 1

echo.
echo [2/4] Running internal validation cases...
python -m core.validation_cases
if errorlevel 1 exit /b 1

echo.
echo [3/4] Validating baseline JSON...
python -m json.tool examples\ai_soc_5ghz_baseline.json > nul
if errorlevel 1 exit /b 1

echo.
echo [4/4] Checking Streamlit app syntax...
python -m py_compile app.py
if errorlevel 1 exit /b 1

echo.
echo ============================================================
echo FULL VALIDATION PASSED
echo Project is ready for GitHub publishing.
echo ============================================================

endlocal