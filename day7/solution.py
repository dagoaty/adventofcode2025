#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 7
Line splitting simulation on a grid
"""

import sys


def parse_input(filename: str) -> list[str]:
    """
    Parse input file into a grid (list of strings).

    Args:
        filename: Path to input file

    Returns:
        List of strings representing the grid
    """
    with open(filename, 'r') as f:
        return [line.rstrip('\n') for line in f]


def find_start(grid: list[str]) -> tuple[int, int]:
    """
    Find the position of 'S' in the grid.

    Args:
        grid: The input grid

    Returns:
        Tuple of (row, col) where S is located

    Raises:
        ValueError: If S is not found
    """
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                return (row_idx, col_idx)
    raise ValueError("Start position 'S' not found in grid")


def get_split_positions(col: int, num_cols: int) -> list[int]:
    """
    Get valid column positions for a split (col-1 and col+1).

    When a line at column position 'col' hits a '^' and splits,
    it creates two new lines at adjacent columns (col-1 and col+1),
    but only if those positions are within grid bounds.

    Args:
        col: Current column position
        num_cols: Total number of columns in grid

    Returns:
        List of valid column positions (within bounds [0, num_cols))
    """
    positions = []
    if col - 1 >= 0:
        positions.append(col - 1)
    if col + 1 < num_cols:
        positions.append(col + 1)
    return positions


def simulate_line_splits(grid: list[str], start_row: int, start_col: int, debug: bool = False) -> int:
    """
    Simulate lines traveling south from start position, splitting when they hit '^'.

    When a line at (row, col) hits a '^':
    - The line terminates
    - Two new lines spawn at (row, col-1) and (row, col+1)
    - These new lines continue south
    - Lines at the same position automatically merge

    Args:
        grid: The input grid
        start_row: Starting row position
        start_col: Starting column position
        debug: If True, print debug information

    Returns:
        Total number of splits that occurred
    """
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    # Track active columns at current row
    active_columns = {start_col}
    total_splits = 0

    if debug:
        print(f"Starting at row {start_row}, col {start_col}")
        print(f"Grid: {num_rows} rows x {num_cols} cols")

    # Process each row from start to bottom
    for row in range(start_row + 1, num_rows):
        new_active = set()
        row_splits = 0

        for col in active_columns:
            # Check if this column is within bounds
            if 0 <= col < num_cols:
                if grid[row][col] == '^':
                    # Line hits '^' - split occurs
                    row_splits += 1

                    # Add new lines at split positions (col-1 and col+1)
                    for new_col in get_split_positions(col, num_cols):
                        new_active.add(new_col)
                else:
                    # Line continues to next row
                    new_active.add(col)

        total_splits += row_splits
        active_columns = new_active

        if debug and row_splits > 0:
            print(f"Row {row}: {row_splits} splits, active columns: {sorted(active_columns)}")

        # If no active columns remain, we're done
        if not active_columns:
            if debug:
                print(f"All lines terminated at row {row}")
            break

    return total_splits


def count_line_paths(grid: list[str], start_row: int, start_col: int, debug: bool = False) -> int:
    """
    Count total number of distinct line paths (without merging).

    Each time a line hits a '^', it splits into two independent paths.
    We track the multiplicity (count) of lines at each position.
    Lines at the same position are counted separately (no merging).

    Args:
        grid: The input grid
        start_row: Starting row position
        start_col: Starting column position
        debug: If True, print debug information

    Returns:
        Total number of distinct line paths
    """
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    # Track line counts at each column: {column: number of lines at that column}
    active_positions = {start_col: 1}

    if debug:
        print(f"\nPart 2: Counting distinct line paths")
        print(f"Starting at row {start_row}, col {start_col} with 1 line")

    # Process each row from start to bottom
    for row in range(start_row + 1, num_rows):
        new_active = {}

        for col, count in active_positions.items():
            # Check if this column is within bounds
            if 0 <= col < num_cols:
                if grid[row][col] == '^':
                    # Each of the 'count' lines at this position splits into 2
                    # Add count lines to each split position (col-1 and col+1)
                    for new_col in get_split_positions(col, num_cols):
                        new_active[new_col] = new_active.get(new_col, 0) + count
                else:
                    # Lines continue to next row at same column
                    new_active[col] = new_active.get(col, 0) + count

        active_positions = new_active

        if debug and active_positions:
            total_lines = sum(active_positions.values())
            print(f"Row {row}: {len(active_positions)} positions, {total_lines} total lines")

        # If no active positions remain, we're done
        if not active_positions:
            if debug:
                print(f"All lines terminated at row {row}")
            return 0

    # Sum up all line counts across all final positions
    total_paths = sum(active_positions.values())
    return total_paths


def main():
    """Main function to run the solution."""
    import argparse

    parser = argparse.ArgumentParser(description='Day 7: Line Splitting Simulation')
    parser.add_argument('filename', nargs='?', default='input.test',
                       help='Input file (default: input.test)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug output')

    args = parser.parse_args()

    # Parse input
    grid = parse_input(args.filename)

    # Find start position
    start_row, start_col = find_start(grid)

    # Part 1: Count total splits
    total_splits = simulate_line_splits(grid, start_row, start_col, args.debug)
    print(f"Part 1: Total splits = {total_splits}")

    # Part 2: Count distinct line paths (no merging)
    total_paths = count_line_paths(grid, start_row, start_col, args.debug)
    print(f"Part 2: Total line paths = {total_paths}")


if __name__ == "__main__":
    main()
