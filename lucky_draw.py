"""
Lucky Draw Number Generator

This module provides functionality to generate random 10-digit numbers for lucky draw events.
"""

import random
from typing import List, Set


def generate_lucky_draw_numbers(count: int = 10, ensure_unique: bool = True) -> List[int]:
    """
    Generate random 10-digit numbers for a lucky draw.

    Args:
        count (int): The number of lucky draw numbers to generate. Default is 10.
        ensure_unique (bool): If True, ensures all generated numbers are unique. Default is True.

    Returns:
        List[int]: A list of randomly generated 10-digit numbers.

    Raises:
        ValueError: If count is negative or exceeds the maximum possible unique 10-digit numbers.

    Examples:
        >>> numbers = generate_lucky_draw_numbers(5)
        >>> len(numbers)
        5
        >>> all(1000000000 <= num <= 9999999999 for num in numbers)
        True
    """
    if count < 0:
        raise ValueError("Count must be a non-negative integer")

    # Maximum possible unique 10-digit numbers: 9,000,000,000
    # (from 1,000,000,000 to 9,999,999,999)
    max_unique = 9_000_000_000

    if ensure_unique and count > max_unique:
        raise ValueError(f"Cannot generate {count} unique 10-digit numbers. Maximum is {max_unique}")

    if count == 0:
        return []

    lucky_numbers: List[int] = []

    if ensure_unique:
        # Use a set to track generated numbers and ensure uniqueness
        generated: Set[int] = set()

        while len(generated) < count:
            # Generate a random 10-digit number (1,000,000,000 to 9,999,999,999)
            number = random.randint(1_000_000_000, 9_999_999_999)
            generated.add(number)

        lucky_numbers = list(generated)
    else:
        # Generate numbers without uniqueness constraint
        for _ in range(count):
            number = random.randint(1_000_000_000, 9_999_999_999)
            lucky_numbers.append(number)

    return lucky_numbers


def display_lucky_draw_numbers(numbers: List[int]) -> None:
    """
    Display the lucky draw numbers in a formatted manner.

    Args:
        numbers (List[int]): List of lucky draw numbers to display.
    """
    print("=" * 50)
    print("LUCKY DRAW NUMBERS")
    print("=" * 50)

    for i, number in enumerate(numbers, 1):
        print(f"Number {i:2d}: {number:,}")

    print("=" * 50)


if __name__ == "__main__":
    # Example usage: Generate 10 unique lucky draw numbers
    print("Generating 10 lucky draw numbers...\n")

    lucky_numbers = generate_lucky_draw_numbers(count=10, ensure_unique=True)
    display_lucky_draw_numbers(lucky_numbers)

    print("\n\nGenerating 5 more lucky draw numbers (duplicates allowed)...\n")
    more_numbers = generate_lucky_draw_numbers(count=5, ensure_unique=False)
    display_lucky_draw_numbers(more_numbers)
