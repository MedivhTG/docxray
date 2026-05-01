@echo off

for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"
set "RED=%ESC%[31m"
set "RESET=%ESC%[0m"

echo %RED%^>^>^> run coverage ^<^<^<%RESET%
echo %RED%!!! SOME MISSING LINES ACTUALLY EXECUTED IN TESTS BUT NOT COUNT AS COVERED IN COVERAGE !!!%RESET%

coverage run -m pytest ./tests
if %errorlevel% neq 0 (
    echo %RED%test coverage failed%RESET%
    exit /b 1
)

coverage report -m
if %errorlevel% neq 0 (
    echo %RED%test failed%RESET%
    exit /b 1
)

coverage xml -o coverage.xml
if %errorlevel% neq 0 (
    echo %RED%test failed%RESET%
    exit /b 1
)

echo %RED%!!! SOME MISSING LINES ACTUALLY EXECUTED IN TESTS BUT NOT COUNT AS COVERED IN COVERAGE !!!%RESET%