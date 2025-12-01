@echo off
REM ============================================
REM Quick Update - For existing repositories
REM ============================================

echo Updating AppleTrader Pro code...

git fetch origin
git checkout claude/recover-appletrader-pro-01CDqrQt2QJVExCCkMbx7iqC
git pull origin claude/recover-appletrader-pro-01CDqrQt2QJVExCCkMbx7iqC

echo.
echo Update complete! Latest changes:
git log -3 --oneline
echo.

pause
