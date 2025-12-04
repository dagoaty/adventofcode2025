#!/usr/bin/env python3

# 8 directions: N, NE, E, SE, S, SW, W, NW
DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def count_neighbors(grid, row, col):
    """
    Count @ neighbors in all 8 directions for a given position.

    Args:
        grid: 2D grid (list of lists or list of strings)
        row: Row index
        col: Column index

    Returns:
        Integer count of @ neighbors
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    neighbor_count = 0

    for dr, dc in DIRECTIONS:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                neighbor_count += 1

    return neighbor_count


def find_symbols_with_few_neighbors(grid, threshold=4):
    """
    Find all @ symbols with fewer than threshold neighbors.

    Args:
        grid: 2D grid (list of lists or list of strings)
        threshold: Maximum neighbor count (exclusive)

    Returns:
        List of (row, col) tuples for @ symbols with < threshold neighbors
    """
    if not grid:
        return []

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    positions = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                neighbor_count = count_neighbors(grid, row, col)
                if neighbor_count < threshold:
                    positions.append((row, col))

    return positions


def count_isolated_at_symbols(grid, debug=False):
    """
    Count @ symbols that have fewer than 4 @ neighbors in 8 directions.

    Args:
        grid: List of strings representing the grid
        debug: Boolean flag for debug output

    Returns:
        Integer count of @ symbols with < 4 @ neighbors
    """
    positions = find_symbols_with_few_neighbors(grid, threshold=4)

    if debug:
        for row, col in positions:
            neighbor_count = count_neighbors(grid, row, col)
            print(f"@ at ({row}, {col}) has {neighbor_count} neighbors - COUNTED")

    return len(positions)


def iterative_removal(grid, debug=False):
    """
    Iteratively remove @ symbols with <4 neighbors until no more can be removed.

    Args:
        grid: List of strings representing the grid
        debug: Boolean flag for debug output

    Returns:
        Integer total count of @ symbols removed across all iterations
    """
    if not grid:
        return 0

    # Convert grid to mutable structure (list of lists)
    mutable_grid = [list(row) for row in grid]
    total_removed = 0
    iteration = 0

    while True:
        iteration += 1
        # Find all @ symbols with < 4 neighbors
        to_remove = find_symbols_with_few_neighbors(mutable_grid, threshold=4)

        # If no symbols to remove, we're done
        if not to_remove:
            if debug:
                print(f"\nIteration {iteration}: No more @ symbols to remove")
            break

        # Remove all marked symbols
        for row, col in to_remove:
            mutable_grid[row][col] = '.'

        total_removed += len(to_remove)

        if debug:
            print(f"\nIteration {iteration}: Removed {len(to_remove)} @ symbols")
            print(f"Running total: {total_removed}")

    return total_removed


def main():
    """Main function to handle argument parsing and execution."""
    import sys

    # Parse arguments
    filename = "input"
    debug = False

    args = sys.argv[1:]
    for arg in args:
        if arg == "--debug":
            debug = True
        elif not arg.startswith("--"):
            filename = arg

    # Read input
    try:
        with open(filename, 'r') as f:
            grid = [line.rstrip('\n') for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    if debug:
        print(f"Grid dimensions: {len(grid)} rows x {len(grid[0]) if grid else 0} cols")
        print()

    # Part 1
    result_part1 = count_isolated_at_symbols(grid, debug)
    print(f"Part 1: {result_part1}")

    # Part 2
    result_part2 = iterative_removal(grid, debug)
    print(f"Part 2: {result_part2}")


if __name__ == "__main__":
    main()
