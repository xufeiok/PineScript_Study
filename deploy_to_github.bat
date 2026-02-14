@echo off
setlocal

echo ===================================================
echo   Pine Script Study System - GitHub Deployment Tool
echo ===================================================

rem Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH.
    pause
    exit /b
)

rem Check if remote 'origin' exists
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Please create a new empty repository on GitHub first.
    echo.
    set /p "REPO_URL=Enter your GitHub Repository URL (e.g., https://github.com/user/repo.git): "
    
    if "%REPO_URL%"=="" (
        echo Error: URL cannot be empty.
        pause
        exit /b
    )
    
    git remote add origin %REPO_URL%
) else (
    echo Remote 'origin' already configured.
)

echo.
echo [Step 1] Pushing main branch code...
git push -u origin main

echo.
echo [Step 2] Deploying 'web' folder to 'gh-pages' branch...
echo (This creates/updates the webpage content)
git subtree push --prefix web origin gh-pages

echo.
echo ===================================================
echo Deployment Complete!
echo.
echo [Next Steps on GitHub]
echo 1. Go to your repository Settings -> Pages
echo 2. Under 'Build and deployment', ensure Source is 'Deploy from a branch'
echo 3. Select Branch: 'gh-pages', Folder: '/ (root)'
echo 4. Click Save
echo.
echo Your website will be live at: https://<username>.github.io/<repo-name>/
echo ===================================================
pause
