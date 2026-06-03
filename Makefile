export
-include .env

SHELL = /bin/bash

test:
	./scripts/test.sh

test_win:
	.\scripts\test_win.bat

check: 
	./scripts/ruff_mypy.sh

check_win: 
	.\scripts\ruff_mypy_win.bat

format_check: 
	./scripts/format_check.sh

format_check_win:
	.\scripts\format_check_win.bat

format: 
	./scripts/format.sh

format_win: 
	.\scripts\format_win.bat