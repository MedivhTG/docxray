echo -e '\033[31m >>> run isort <<< \033[0m'
isort ./src --profile black --check-only || { echo -e '\033[31m isort failed \033[0m' ; exit 1; }
echo -e '\033[31m >>> run black <<< \033[0m'
black ./src --check || { echo -e '\033[31m test black failed \033[0m' ; exit 1; }