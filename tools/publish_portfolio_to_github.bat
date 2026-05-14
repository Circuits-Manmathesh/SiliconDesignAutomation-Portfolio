@echo off
setlocal

cd /d "%~dp0.."

python tools\check_public_export_safety.py
if errorlevel 1 (
    echo Safety check failed. Fix the public export before publishing.
    exit /b 1
)

if not exist .git (
    git init
)

git branch -M main
git add .
git commit -m "Update SiliconDesignAutomation public portfolio"

git remote get-url origin >nul 2>nul
if errorlevel 1 (
    git remote add origin https://github.com/Circuits-Manmathesh/SiliconDesignAutomation-Portfolio.git
)

git push -u origin main
endlocal
