@echo off
echo ========================================
echo Gradle Setup for Green Scan App
echo ========================================
echo.

REM Create Gradle directory
if not exist "C:\Gradle" mkdir "C:\Gradle"

echo Downloading Gradle 8.5...
echo This may take a few minutes depending on your connection.
echo.

REM Download Gradle using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://services.gradle.org/distributions/gradle-8.5-bin.zip' -OutFile 'C:\Gradle\gradle-8.5-bin.zip' -UseBasicParsing}"

if not exist "C:\Gradle\gradle-8.5-bin.zip" (
    echo ERROR: Download failed!
    echo Please download manually from: https://gradle.org/releases/
    echo Download gradle-8.5-bin.zip and place it in C:\Gradle\
    pause
    exit /b 1
)

echo.
echo Extracting Gradle...
powershell -Command "& {Expand-Archive -Path 'C:\Gradle\gradle-8.5-bin.zip' -DestinationPath 'C:\Gradle' -Force}"

if exist "C:\Gradle\gradle-8.5" (
    echo.
    echo ========================================
    echo SUCCESS! Gradle installed to C:\Gradle\gradle-8.5
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Open Android Studio
    echo 2. Go to File ^> Settings ^> Build Tools ^> Gradle
    echo 3. Select "Use Gradle from: 'specified location'"
    echo 4. Browse to: C:\Gradle\gradle-8.5
    echo 5. Set Gradle JDK to: Embedded JDK
    echo 6. Click Apply and OK
    echo 7. Open the WeedDetectorApp project
    echo.
) else (
    echo ERROR: Extraction failed!
    echo Please extract manually.
)

pause
