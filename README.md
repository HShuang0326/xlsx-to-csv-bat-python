# Batch XLSX to CSV Converter

Batch convert all `.xlsx` files under a target directory into `.csv` files.

Features:

- Recursively scans the target directory and all subfolders
- Skips temporary Excel files such as `~$example.xlsx`
- Exports each worksheet as a separate CSV when a workbook has multiple sheets
- Preserves the original folder structure in the output directory
- Includes both a Python script and a BAT launcher for Windows

## Files

- `convert_xlsx_to_csv.py`
  - Main conversion script
- `convert_xlsx_to_csv.bat`
  - Windows batch launcher

## Requirements

- Windows
- Python 3
- Python packages:
  - `pandas`
  - `openpyxl`

Install dependencies:

```bat
py -3 -m pip install pandas openpyxl
```

If `py` is not available, use:

```bat
python -m pip install pandas openpyxl
```

## Usage

### Method 1: Run the BAT file

```bat
convert_xlsx_to_csv.bat "D:\excel_files"
```

Specify a custom output directory:

```bat
convert_xlsx_to_csv.bat "D:\excel_files" "D:\csv_output"
```

### Method 2: Run the Python script directly

```bat
py -3 convert_xlsx_to_csv.py "D:\excel_files"
```

Specify a custom output directory:

```bat
py -3 convert_xlsx_to_csv.py "D:\excel_files" "D:\csv_output"
```

## Output Rules

Default output directory:

```text
<source_dir>\csv_output
```

If a workbook has only one worksheet:

```text
sales.xlsx -> sales.csv
```

If a workbook has multiple worksheets:

```text
sales.xlsx
-> sales__01_Sheet1.csv
-> sales__02_Summary.csv
```

CSV files are written with `UTF-8 with BOM`, which is usually easier to open directly in Excel on Windows.

## Example

Source folder:

```text
D:\excel_files
|-- report1.xlsx
`-- subfolder
    `-- report2.xlsx
```

Run:

```bat
convert_xlsx_to_csv.bat "D:\excel_files"
```

Possible output:

```text
D:\excel_files\csv_output
|-- report1.csv
`-- subfolder
    `-- report2.csv
```

## Notes

- This script handles `.xlsx` files, not `.xls`
- Workbooks with multiple worksheets are split into multiple CSV files
- If one file fails to convert, the script continues with the remaining files and prints a failure summary at the end

## License

If you plan to publish this repository on GitHub, `MIT License` is a common choice.
