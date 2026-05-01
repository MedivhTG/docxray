echo -e '\033[31m ======== run tests ======== \033[0m'
echo -e '\033[31m >>> run ruff <<< \033[0m'
ruff check ./src || { echo -e '\033[31m test ruff failed \033[0m' ; exit 1; }
echo -e '\033[31m >>> run mypy <<< \033[0m'
mypy --check-untyped-defs ./src || { echo -e '\033[31m test mypy failed \033[0m' ; exit 1; }
