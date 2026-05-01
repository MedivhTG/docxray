SHELL = /bin/bash

check: 
	./src/scripts/ruff_mypy.sh

check_win: 
	.\src\scripts\ruff_mypy_win.bat

format_check: 
	./src/scripts/format_check.sh

format_check_win:
	.\src\scripts\format_check_win.bat

format: 
	./src/scripts/format.sh

format_win: 
	.\src\scripts\format_win.bat