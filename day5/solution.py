#!/usr/bin/env python3

import sys


def parse_input(filename):
    """
    Parse input file into ranges and numbers.

    Args:
        filename: Path to input file

    Returns:
        tuple: (ranges, numbers) where ranges is list of (start, end) tuples
               and numbers is list of integers to check
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # Find blank line separator
    blank_idx = lines.index('')

    # Parse ranges (format: start-end)
    ranges = []
    for line in lines[:blank_idx]:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))

    # Parse numbers to check
    numbers = [int(line) for line in lines[blank_idx + 1:] if line]

    return ranges, numbers


def merge_ranges(ranges):
    """
    Merge overlapping and adjacent ranges.

    Args:
        ranges: List of (start, end) tuples

    Returns:
        List of non-overlapping (start, end) tuples, sorted by start position
    """
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    # Merge overlapping and adjacent ranges
    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        prev_start, prev_end = merged[-1]

        # Check if current range overlaps or touches previous range
        # Ranges touch if current_start = prev_end + 1
        # Ranges overlap if current_start <= prev_end
        if current_start <= prev_end + 1:
            # Merge: extend previous range to cover current range
            merged[-1] = (prev_start, max(prev_end, current_end))
        else:
            # No overlap or touch: add as separate range
            merged.append((current_start, current_end))

    return merged


def is_in_any_range(num, merged_ranges):
    """
    Check if a number falls within any of the merged ranges.

    Args:
        num: Integer to check
        merged_ranges: Sorted list of non-overlapping (start, end) tuples

    Returns:
        bool: True if num is in any range, False otherwise
    """
    for start, end in merged_ranges:
        if start <= num <= end:
            return True
    return False


def count_numbers_in_ranges(merged_ranges, numbers, debug=False):
    """
    Count how many numbers from the list appear in any range.

    Args:
        merged_ranges: List of merged (start, end) tuples
        numbers: List of integers to check
        debug: Whether to print debug information

    Returns:
        int: Count of numbers that appear in any range
    """
    count = 0
    for num in numbers:
        in_range = is_in_any_range(num, merged_ranges)
        if in_range:
            count += 1
            if debug:
                print(f"{num}: in a range")
        elif debug:
            print(f"{num}: NOT in any range")

    return count


def count_total_integers_in_ranges(merged_ranges, debug=False):
    """
    Count total number of integers covered by all ranges.

    Args:
        merged_ranges: List of merged (start, end) tuples
        debug: Whether to print debug information

    Returns:
        int: Total count of integers in all ranges
    """
    total = 0

    if debug:
        print(f"\nPart 2 calculation:")

    for start, end in merged_ranges:
        count = end - start + 1
        total += count
        if debug:
            print(f"  Range [{start}, {end}]: {count} integers")

    return total


def main():
    """Main function to run both parts of the solution."""
    # Parse command line arguments
    debug = '--debug' in sys.argv

    # Determine input file
    args = [arg for arg in sys.argv[1:] if arg != '--debug']
    filename = args[0] if args else 'input'

    # Parse input
    ranges, numbers = parse_input(filename)

    # Merge overlapping and adjacent ranges once
    merged_ranges = merge_ranges(ranges)

    if debug:
        print(f"Loaded {len(ranges)} ranges and {len(numbers)} numbers")
        print(f"After merging: {len(merged_ranges)} ranges")
        print(f"Merged ranges: {merged_ranges}")
        print()

    # Part 1: Count how many numbers from the list appear in ranges
    part1_result = count_numbers_in_ranges(merged_ranges, numbers, debug)
    print(f"Part 1: {part1_result}")

    # Part 2: Count total integers covered by all ranges
    part2_result = count_total_integers_in_ranges(merged_ranges, debug)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
