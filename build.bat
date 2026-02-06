@echo off
REM DocFlow Pro Build Script for Windows

echo ========================================
echo DocFlow Pro - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [2/4] Running core functionality test...
python test_core.py
if errorlevel 1 (
    echo.
    echo Warning: Tests failed but continuing with build...
    echo.
)

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller docflowpro.spec --clean

echo.
echo [4/4] Build complete!
echo.

if exist "dist\DocFlowPro\DocFlowPro.exe" (
    echo ========================================
    echo SUCCESS! Executable created at:
    echo dist\DocFlowPro\DocFlowPro.exe
    echo ========================================
    echo.
    echo You can now run the application by executing:
    echo dist\DocFlowPro\DocFlowPro.exe
    echo.
) else (
    echo ========================================
    echo ERROR: Build failed!
    echo Please check the output above for errors.
    echo ========================================
)

pause
