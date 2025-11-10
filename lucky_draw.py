#!/usr/bin/env python3
"""
Lucky Draw Number Generator

This script generates random 10-digit numbers for lucky draw purposes.
"""

import random
import argparse
from datetime import datetime


def generate_lucky_numbers(count=10, min_digits=10, max_digits=10, unique=True, seed=None):
    """
    Generate random numbers for lucky draw.

    Args:
        count (int): Number of lucky draw numbers to generate (default: 10)
        min_digits (int): Minimum number of digits (default: 10)
        max_digits (int): Maximum number of digits (default: 10)
        unique (bool): Ensure all numbers are unique (default: True)
        seed (int, optional): Random seed for reproducibility

    Returns:
        list: List of generated lucky draw numbers
    """
    if seed is not None:
        random.seed(seed)

    lucky_numbers = []

    # Calculate range for 10-digit numbers
    min_value = 10 ** (min_digits - 1)
    max_value = (10 ** max_digits) - 1

    if unique:
        # Generate unique numbers
        if count > (max_value - min_value + 1):
            raise ValueError(f"Cannot generate {count} unique numbers in the given range")

        lucky_numbers = random.sample(range(min_value, max_value + 1), count)
    else:
        # Generate numbers (may have duplicates)
        for _ in range(count):
            lucky_numbers.append(random.randint(min_value, max_value))

    return sorted(lucky_numbers)


def format_lucky_number(number, separator='-'):
    """
    Format lucky number with separators for better readability.

    Args:
        number (int): The lucky number
        separator (str): Character to use as separator (default: '-')

    Returns:
        str: Formatted number
    """
    num_str = str(number)
    # Split into groups of 3 from right to left
    groups = []
    for i in range(len(num_str), 0, -3):
        groups.insert(0, num_str[max(0, i-3):i])
    return separator.join(groups)


def save_to_file(numbers, filename=None):
    """
    Save lucky numbers to a file.

    Args:
        numbers (list): List of lucky numbers
        filename (str, optional): Output filename
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lucky_draw_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write("=" * 50 + "\n")
        f.write("LUCKY DRAW NUMBERS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")

        for idx, number in enumerate(numbers, 1):
            formatted = format_lucky_number(number)
            f.write(f"{idx:2d}. {number:10d}  ({formatted})\n")

        f.write("\n" + "=" * 50 + "\n")

    print(f"Lucky numbers saved to: {filename}")


def display_numbers(numbers, show_formatted=True):
    """
    Display lucky numbers to console.

    Args:
        numbers (list): List of lucky numbers
        show_formatted (bool): Show formatted version with separators
    """
    print("\n" + "=" * 50)
    print("LUCKY DRAW NUMBERS")
    print("=" * 50 + "\n")

    for idx, number in enumerate(numbers, 1):
        if show_formatted:
            formatted = format_lucky_number(number)
            print(f"{idx:2d}. {number:10d}  ({formatted})")
        else:
            print(f"{idx:2d}. {number:10d}")

    print("\n" + "=" * 50)


def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate random 10-digit numbers for lucky draw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python lucky_draw.py
  python lucky_draw.py --count 20
  python lucky_draw.py --count 10 --save results.txt
  python lucky_draw.py --count 15 --seed 12345
        """
    )

    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Number of lucky numbers to generate (default: 10)'
    )

    parser.add_argument(
        '--digits',
        type=int,
        default=10,
        help='Number of digits for each lucky number (default: 10)'
    )

    parser.add_argument(
        '--save',
        dest='output_file',
        help='Save results to specified file'
    )

    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )

    parser.add_argument(
        '--allow-duplicates',
        action='store_true',
        help='Allow duplicate numbers'
    )

    parser.add_argument(
        '--no-format',
        action='store_true',
        help='Display numbers without formatting'
    )

    args = parser.parse_args()

    try:
        # Generate lucky numbers
        lucky_numbers = generate_lucky_numbers(
            count=args.count,
            min_digits=args.digits,
            max_digits=args.digits,
            unique=not args.allow_duplicates,
            seed=args.seed
        )

        # Display numbers
        display_numbers(lucky_numbers, show_formatted=not args.no_format)

        # Save to file if requested
        if args.output_file:
            save_to_file(lucky_numbers, args.output_file)

    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
