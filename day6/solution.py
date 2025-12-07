#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 6: Column Operations
Parse columns of numbers with operations and calculate results.

Part 1: Treats each whitespace-separated value as a complete number.
Part 2: Uses character position to preserve visual alignment of digits.
"""
import argparse
import sys
from functools import reduce
from operator import mul, add
from typing import Optional

# Type alias for Part 2 column data structure
# Maps operation position -> (list of transposed numbers, operation char)
ColumnData = dict[int, tuple[list[int], str]]


def parse_input(filename: str) -> list[list[str]]:
    """
    Parse input file into columns of values using whitespace splitting.

    This approach treats each whitespace-separated value as a complete number,
    ignoring visual alignment in the file. Used for Part 1.

    Args:
        filename: Path to input file

    Returns:
        List of columns, where each column is a list of values (numbers + operation)
    """
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    # Parse each line into values (split by whitespace)
    rows = [line.split() for line in lines]

    # Transpose rows into columns
    num_cols = len(rows[0])
    columns = [[rows[row_idx][col_idx] for row_idx in range(len(rows))]
               for col_idx in range(num_cols)]

    return columns


def apply_operation(numbers: list[int], operation: str) -> int:
    """
    Apply an operation (* or +) to a list of numbers.

    Args:
        numbers: List of integers to combine
        operation: Either '*' (multiply) or '+' (add)

    Returns:
        Result of applying the operation to all numbers
    """
    if operation == '*':
        return reduce(mul, numbers, 1)
    elif operation == '+':
        return reduce(add, numbers, 0)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def calculate_column_result(column: list[str]) -> int:
    """
    Calculate the result for a single column.

    The last element is the operation (* or +).
    All other elements are numbers to be combined using that operation.

    Args:
        column: List of string values (numbers + operation at end)

    Returns:
        Result of applying the operation to all numbers
    """
    operation = column[-1]
    numbers = [int(val) for val in column[:-1]]
    return apply_operation(numbers, operation)


def solve_part1(columns: list[list[str]]) -> int:
    """
    Solve Part 1: Calculate sum of all column results.

    Args:
        columns: List of columns with numbers and operations

    Returns:
        Sum of all column results
    """
    column_results = [calculate_column_result(col) for col in columns]
    return sum(column_results)


def collect_digits_by_position(number_lines: list[str], max_pos: int) -> dict[int, list[str]]:
    """
    Collect digits at each character position, reading top to bottom.

    Args:
        number_lines: Lines containing numbers (excluding operation line)
        max_pos: Maximum character position to check

    Returns:
        Dictionary mapping character position to list of digits found at that position
    """
    digits_by_position = {}

    for pos in range(max_pos):
        digits = []
        for line in number_lines:
            if pos < len(line) and line[pos].isdigit():
                digits.append(line[pos])

        if digits:  # Only store if we found any digits
            digits_by_position[pos] = digits

    return digits_by_position


def find_column_for_position(digit_pos: int, operation_positions: list[int]) -> Optional[int]:
    """
    Find which column a digit position belongs to.

    Assigns to the closest operation position that's <= digit_pos.

    Args:
        digit_pos: Character position of a digit
        operation_positions: Sorted list of positions where operations appear

    Returns:
        Operation position this digit belongs to, or None if no match
    """
    for op_pos in reversed(operation_positions):
        if op_pos <= digit_pos:
            return op_pos
    return None


def parse_input_by_position(filename: str) -> ColumnData:
    """
    Parse input file by character position, preserving exact alignment.

    This approach reads each character position vertically to form numbers,
    preserving the visual alignment in the file (leading spaces matter).
    Used for Part 2.

    For example, if the file has:
        123 328
         45  64
          6  98

    Character position 0 has [1, _, _] which forms number 1.
    Character position 1 has [2, 4, _] which forms number 24.
    Character position 2 has [3, 5, 6] which forms number 356.

    Args:
        filename: Path to input file

    Returns:
        Dictionary mapping operation position to (list of transposed numbers, operation)
    """
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]

    # Last line has operations, previous lines have numbers
    operation_line = lines[-1]
    number_lines = lines[:-1]

    # Find operation positions (where * or + appear)
    operations = {}
    for pos, char in enumerate(operation_line):
        if char in ('*', '+'):
            operations[pos] = char

    # Collect digits at each character position
    max_pos = max(len(line) for line in lines)
    digits_by_position = collect_digits_by_position(number_lines, max_pos)

    # Group character positions by their column (based on nearest operation)
    operation_positions = sorted(operations.keys())
    column_data = {op_pos: ([], operations[op_pos]) for op_pos in operation_positions}

    # Assign each digit position to a column and build numbers
    for digit_pos, digits in digits_by_position.items():
        assigned_col = find_column_for_position(digit_pos, operation_positions)

        if assigned_col is not None:
            # Build number from digits (top to bottom)
            number = int(''.join(digits))
            column_data[assigned_col][0].append(number)

    return column_data


def solve_part2(filename: str, debug: bool = False) -> int:
    """
    Solve Part 2: Transform numbers by character position transposition.

    Parse the file by character position, where each character position
    creates a number by reading digits top-to-bottom. Character positions
    are grouped by column based on the operation row.

    Args:
        filename: Path to input file
        debug: Enable debug output

    Returns:
        Sum of all transformed column results
    """
    columns_data = parse_input_by_position(filename)

    results = []
    for op_pos in sorted(columns_data.keys()):
        numbers, operation = columns_data[op_pos]

        if debug:
            print(f"\nColumn at position {op_pos} ({operation}):")
            print(f"  Numbers: {numbers}")

        result = apply_operation(numbers, operation)

        if debug:
            print(f"  Result: {result}")

        results.append(result)

    return sum(results)


def main():
    """Main entry point for the solution."""
    parser = argparse.ArgumentParser(description='Advent of Code 2025 - Day 6')
    parser.add_argument('input_file', nargs='?', default='input',
                        help='Input file (default: input)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug output')
    args = parser.parse_args()

    try:
        columns = parse_input(args.input_file)

        if args.debug:
            print(f"Parsed {len(columns)} columns")
            for i, col in enumerate(columns):
                print(f"Column {i}: {col}")

        # Solve Part 1
        part1_result = solve_part1(columns)
        print(f"Part 1: {part1_result}")

        # Solve Part 2 (uses character position parsing)
        part2_result = solve_part2(args.input_file, debug=args.debug)
        print(f"Part 2: {part2_result}")

    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
