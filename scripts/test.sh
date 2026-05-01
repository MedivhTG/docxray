echo -e '\033[31m >>> run coverage <<< \033[0m'
echo -e '\033[31m !!! SOME MISSING LINES ACTUALLY EXECUTED IN TESTS BUT NOT COUNT AS COVERED IN COVERAGE !!! \033[0m'
coverage run -m pytest ./tests || { echo 'test coverage failed' ; exit 1; }
coverage report -m || { echo -e '\033[31m test failed \033[0m' ; exit 1; }
coverage xml -o coverage.xml || { echo '\033[31m test failed \033[0m' ; exit 1; }
echo -e '\033[31m !!! SOME MISSING LINES ACTUALLY EXECUTED IN TESTS BUT NOT COUNT AS COVERED IN COVERAGE !!! \033[0m'