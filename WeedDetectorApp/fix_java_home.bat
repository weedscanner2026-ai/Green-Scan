@echo off
echo ========================================
echo Fixing JAVA_HOME
echo ========================================
echo.
echo Current JAVA_HOME: %JAVA_HOME%
echo.
echo This is WRONG! It should be C:\jdk-19.0.2 (without \bin)
echo.
echo Fixing it now...
echo.

REM Set JAVA_HOME for current session
set JAVA_HOME=C:\jdk-19.0.2
echo Session JAVA_HOME set to: %JAVA_HOME%
echo.

REM Set JAVA_HOME permanently in system environment
setx JAVA_HOME "C:\jdk-19.0.2" /M

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! JAVA_HOME fixed permanently
    echo ========================================
    echo.
    echo IMPORTANT: You MUST restart your computer for this to take full effect!
    echo.
    echo After restart:
    echo 1. Run setup_gradle.bat
    echo 2. Then open Android Studio
    echo.
) else (
    echo.
    echo ERROR: Could not set system variable (need admin rights)
    echo.
    echo Please do this manually:
    echo 1. Press Windows + R
    echo 2. Type: sysdm.cpl
    echo 3. Press Enter
    echo 4. Go to Advanced tab
    echo 5. Click Environment Variables
    echo 6. Find JAVA_HOME in System variables
    echo 7. Change from: C:\jdk-19.0.2\bin
    echo 8. Change to:   C:\jdk-19.0.2
    echo 9. Click OK on all windows
    echo 10. Restart your computer
    echo.
)

pause
