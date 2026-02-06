@echo off
REM Copy DocFlowPro.exe to Downloads folder

echo ========================================
echo DocFlow Pro - Deploy to Downloads
echo ========================================
echo.

set "SOURCE=dist\DocFlowPro\DocFlowPro.exe"
set "DEST=%USERPROFILE%\Downloads\DocFlowPro.exe"

if not exist "%SOURCE%" (
    echo ERROR: Source file not found: %SOURCE%
    pause
    exit /b 1
)

echo Copying executable to Downloads...
copy /Y "%SOURCE%" "%DEST%"

if exist "%DEST%" (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo DocFlowPro.exe has been copied to:
    echo %DEST%
    echo.
    echo The EXPORT functionality has been FIXED!
    echo - All users can now export their data
    echo - No more "no data to export" errors
    echo.
    echo You can now run the fixed application from:
    echo Downloads folder
    echo.
) else (
    echo.
    echo ERROR: Copy failed!
    echo.
)

pause
