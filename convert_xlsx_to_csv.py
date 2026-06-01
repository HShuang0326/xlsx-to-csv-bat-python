from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd


INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]+')


def sanitize_filename(name: str) -> str:
    cleaned = INVALID_FILENAME_CHARS.sub("_", name).strip()
    return cleaned or "Sheet"


def convert_workbook(source_file: Path, source_root: Path, output_root: Path) -> list[Path]:
    excel_file = pd.ExcelFile(source_file)
    target_dir = output_root / source_file.parent.relative_to(source_root)
    target_dir.mkdir(parents=True, exist_ok=True)

    exported_files: list[Path] = []
    multiple_sheets = len(excel_file.sheet_names) > 1

    for index, sheet_name in enumerate(excel_file.sheet_names, start=1):
        dataframe = pd.read_excel(excel_file, sheet_name=sheet_name)

        if multiple_sheets:
            csv_name = f"{source_file.stem}__{index:02d}_{sanitize_filename(sheet_name)}.csv"
        else:
            csv_name = f"{source_file.stem}.csv"

        output_file = target_dir / csv_name
        dataframe.to_csv(output_file, index=False, encoding="utf-8-sig")
        exported_files.append(output_file)

    return exported_files


def find_xlsx_files(source_root: Path) -> list[Path]:
    return sorted(
        file_path
        for file_path in source_root.rglob("*.xlsx")
        if file_path.is_file() and not file_path.name.startswith("~$")
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Batch convert all .xlsx files under a directory to .csv files."
    )
    parser.add_argument("source_dir", help="Directory containing xlsx files")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Directory for csv output. Defaults to <source_dir>\\csv_output",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_root = Path(args.source_dir).expanduser().resolve()
    if not source_root.exists() or not source_root.is_dir():
        print(f"Source directory does not exist: {source_root}")
        return 1

    output_root = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else (source_root / "csv_output").resolve()
    )
    output_root.mkdir(parents=True, exist_ok=True)

    xlsx_files = find_xlsx_files(source_root)
    if not xlsx_files:
        print(f"No .xlsx files found under: {source_root}")
        return 0

    converted_count = 0
    failed_files: list[tuple[Path, str]] = []

    for source_file in xlsx_files:
        try:
            exported_files = convert_workbook(source_file, source_root, output_root)
            converted_count += len(exported_files)
            print(f"[OK] {source_file}")
            for exported_file in exported_files:
                print(f"     -> {exported_file}")
        except Exception as exc:  # noqa: BLE001
            failed_files.append((source_file, str(exc)))
            print(f"[FAIL] {source_file}")
            print(f"       {exc}")

    print()
    print(f"Processed workbooks: {len(xlsx_files)}")
    print(f"Generated csv files: {converted_count}")
    print(f"Output directory: {output_root}")

    if failed_files:
        print()
        print("Failed files:")
        for source_file, reason in failed_files:
            print(f"- {source_file}: {reason}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
