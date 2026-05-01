@echo off

for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m"
set "RESET=%ESC%[0m"

echo %RED%^>^>^> run isort ^<^<^<%RESET%
isort ./src --profile black --check-only
if %errorlevel% neq 0 (
    echo %RED%isort failed%RESET%
    exit /b 1
)

echo %RED%^>^>^> run black ^<^<^<%RESET%
black ./src --check
if %errorlevel% neq 0 (
    echo %RED%test black failed%RESET%
    exit /b 1
)