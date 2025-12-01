@echo off
REM ============================================
REM AppleTrader Pro - Code Sync Batch File
REM Pulls latest code from Claude's development branch
REM ============================================

echo.
echo ========================================
echo  AppleTrader Pro - Code Sync
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git is not installed or not in PATH!
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

REM Configuration
set REPO_URL=https://github.com/Superuser2025/MagicBranch.git
set BRANCH_NAME=claude/recover-appletrader-pro-01CDqrQt2QJVExCCkMbx7iqC
set LOCAL_DIR=MagicBranch

echo [1/4] Checking repository status...
echo.

REM Check if directory exists
if exist "%LOCAL_DIR%" (
    echo Found existing repository at: %CD%\%LOCAL_DIR%
    echo.

    cd "%LOCAL_DIR%"

    echo [2/4] Fetching latest changes from GitHub...
    git fetch origin
    if %errorlevel% neq 0 (
        echo ERROR: Failed to fetch from remote!
        cd ..
        pause
        exit /b 1
    )
    echo.

    echo [3/4] Checking out branch: %BRANCH_NAME%
    git checkout %BRANCH_NAME%
    if %errorlevel% neq 0 (
        echo ERROR: Failed to checkout branch!
        cd ..
        pause
        exit /b 1
    )
    echo.

    echo [4/4] Pulling latest code...
    git pull origin %BRANCH_NAME%
    if %errorlevel% neq 0 (
        echo ERROR: Failed to pull changes!
        cd ..
        pause
        exit /b 1
    )

    cd ..
) else (
    echo Repository not found locally. Cloning...
    echo.

    echo [2/4] Cloning repository from GitHub...
    git clone %REPO_URL% %LOCAL_DIR%
    if %errorlevel% neq 0 (
        echo ERROR: Failed to clone repository!
        echo Make sure you have access to: %REPO_URL%
        pause
        exit /b 1
    )
    echo.

    cd "%LOCAL_DIR%"

    echo [3/4] Checking out branch: %BRANCH_NAME%
    git checkout %BRANCH_NAME%
    if %errorlevel% neq 0 (
        echo ERROR: Failed to checkout branch!
        cd ..
        pause
        exit /b 1
    )
    echo.

    echo [4/4] Repository setup complete!

    cd ..
)

echo.
echo ========================================
echo  SUCCESS! Code sync completed
echo ========================================
echo.

cd "%LOCAL_DIR%"

echo Latest commits on this branch:
echo.
git log -5 --oneline --decorate
echo.

echo Files in Apple/python/widgets/ directory:
echo.
dir /b Apple\python\widgets\*.py 2>nul
echo.

cd ..

echo ========================================
echo Repository location: %CD%\%LOCAL_DIR%
echo Branch: %BRANCH_NAME%
echo.
echo All 10 AppleTrader Pro improvements are now available!
echo ========================================
echo.

pause
