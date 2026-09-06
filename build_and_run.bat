@echo off
echo ========================================
echo Building FitBuddy Docker Image
echo ========================================

docker build -t fitbuddy-app .

if %ERRORLEVEL% NEQ 0 (
    echo Docker build failed!
    exit /b 1
)

echo ========================================
echo Running FitBuddy Container
echo ========================================
echo App will be available at http://localhost:7860
echo Press Ctrl+C to stop the container
echo ========================================

docker run -p 7860:7860 --env-file .env fitbuddy-app
