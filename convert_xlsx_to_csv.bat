@echo off
setlocal

if "%~1"=="" (
    echo Usage: %~nx0 "source_dir" ["output_dir"]
    echo Example: %~nx0 "D:\excel_files" "D:\csv_files"
    exit /b 1
)

set "SCRIPT_DIR=%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    py -3 "%SCRIPT_DIR%convert_xlsx_to_csv.py" %*
    exit /b %errorlevel%
)

python "%SCRIPT_DIR%convert_xlsx_to_csv.py" %*
exit /b %errorlevel%
