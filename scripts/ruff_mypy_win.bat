@echo off

:: Получаем ANSI escape-символ для цветов
for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m"
set "RESET=%ESC%[0m"

echo %RED%======== run tests ========%RESET%

echo %RED%^>^>^> run ruff ^<^<^<%RESET%
ruff check ./src
if %errorlevel% neq 0 (
    echo %RED%test ruff failed%RESET%
    exit /b 1
)

echo %RED%^>^>^> run mypy ^<^<^<%RESET%
mypy --check-untyped-defs ./src
if %errorlevel% neq 0 (
    echo %RED%test mypy failed%RESET%
    exit /b 1
)