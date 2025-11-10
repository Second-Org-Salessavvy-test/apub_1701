#!/usr/bin/env python3
"""
Data Cleaner - Remove null values from CSV files

This script reads a CSV file and removes rows containing null/empty values,
then saves the cleaned data to a new CSV file.
"""

import pandas as pd
import argparse
import sys
from pathlib import Path


def clean_csv(input_file, output_file=None, drop_columns=False):
    """
    Remove null values from a CSV file.

    Args:
        input_file (str): Path to the input CSV file
        output_file (str, optional): Path to the output CSV file.
                                     If None, defaults to input_file_cleaned.csv
        drop_columns (bool): If True, drop columns with any null values.
                            If False, drop rows with any null values.

    Returns:
        tuple: (rows_removed, output_path)
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        initial_rows = len(df)
        initial_cols = len(df.columns)

        print(f"Original dataset: {initial_rows} rows, {initial_cols} columns")
        print(f"Null values found: {df.isnull().sum().sum()}")

        # Remove null values
        if drop_columns:
            df_cleaned = df.dropna(axis=1)
            cols_removed = initial_cols - len(df_cleaned.columns)
            print(f"Removed {cols_removed} columns with null values")
        else:
            df_cleaned = df.dropna(axis=0)
            rows_removed = initial_rows - len(df_cleaned)
            print(f"Removed {rows_removed} rows with null values")

        # Determine output file path
        if output_file is None:
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"

        # Save cleaned data
        df_cleaned.to_csv(output_file, index=False)
        print(f"Cleaned dataset: {len(df_cleaned)} rows, {len(df_cleaned.columns)} columns")
        print(f"Saved to: {output_file}")

        return (initial_rows - len(df_cleaned), output_file)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: File '{input_file}' is empty")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Remove null values from CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python data_cleaner.py input.csv
  python data_cleaner.py input.csv -o output.csv
  python data_cleaner.py input.csv --drop-columns
        """
    )

    parser.add_argument(
        'input_file',
        help='Path to the input CSV file'
    )

    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='Path to the output CSV file (default: input_file_cleaned.csv)'
    )

    parser.add_argument(
        '--drop-columns',
        action='store_true',
        help='Drop columns with null values instead of rows'
    )

    args = parser.parse_args()

    clean_csv(args.input_file, args.output_file, args.drop_columns)


if __name__ == "__main__":
    main()
