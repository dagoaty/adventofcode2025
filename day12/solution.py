#!/usr/bin/env python3

import sys
from typing import Set, List, Tuple

DEBUG = False

def debug(*args, **kwargs):
    """Print debug messages if DEBUG flag is enabled."""
    if DEBUG:
        print(*args, **kwargs)

def parse_input(filename: str) -> Tuple[dict[int, Set[Tuple[int, int]]], List[Tuple[int, int, List[int]]]]:
    """
    Parse the input file into tile definitions and test cases.

    Returns:
        tiles: Dictionary mapping tile_id to set of (row, col) coordinates for '#' positions
        test_cases: List of (width, height, tile_counts) tuples
    """
    with open(filename) as f:
        content = f.read().strip()

    sections = content.split('\n\n')

    # Parse tiles (all sections before the last one)
    tiles = {}
    for section in sections[:-1]:
        lines = section.strip().split('\n')
        tile_id = int(lines[0].rstrip(':'))

        coords = set()
        for row, line in enumerate(lines[1:]):
            for col, char in enumerate(line):
                if char == '#':
                    coords.add((row, col))

        tiles[tile_id] = coords

    # Parse test cases (last section)
    test_cases = []
    for line in sections[-1].strip().split('\n'):
        size_part, counts_part = line.split(': ')
        width, height = map(int, size_part.split('x'))
        counts = list(map(int, counts_part.split()))
        test_cases.append((width, height, counts))

    return tiles, test_cases

def rotate_90(coords: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Rotate coordinates 90 degrees clockwise."""
    if not coords:
        return set()

    # Rotate: (r, c) -> (c, -r)
    rotated = {(c, -r) for r, c in coords}

    # Normalize to start from (0, 0)
    min_r = min(r for r, c in rotated)
    min_c = min(c for r, c in rotated)
    return {(r - min_r, c - min_c) for r, c in rotated}

def flip_horizontal(coords: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Flip coordinates horizontally."""
    if not coords:
        return set()

    # Flip: (r, c) -> (r, -c)
    flipped = {(r, -c) for r, c in coords}

    # Normalize to start from (0, 0)
    min_r = min(r for r, c in flipped)
    min_c = min(c for r, c in flipped)
    return {(r - min_r, c - min_c) for r, c in flipped}

def generate_orientations(coords: Set[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    """
    Generate all unique orientations (rotations + flips) of a tile.

    Returns list of unique coordinate sets.
    """
    orientations = []
    seen = set()

    # Generate original and flipped, each with 4 rotations
    for base in [coords, flip_horizontal(coords)]:
        current = base
        for _ in range(4):
            # Convert to frozenset for hashing
            frozen = frozenset(current)
            if frozen not in seen:
                seen.add(frozen)
                orientations.append(current)
            current = rotate_90(current)

    return orientations

def get_bounds(coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """Get the bounding box dimensions of a tile."""
    if not coords:
        return 0, 0

    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return max_r + 1, max_c + 1

def place_tile(coords: Set[Tuple[int, int]], start_r: int, start_c: int) -> Set[Tuple[int, int]]:
    """Translate tile coordinates to absolute grid positions."""
    return {(r + start_r, c + start_c) for r, c in coords}

def can_fit(grid_width: int, grid_height: int, tile_coords: Set[Tuple[int, int]],
            start_r: int, start_c: int, occupied: Set[Tuple[int, int]]) -> bool:
    """Check if a tile can be placed at the given position without conflicts."""
    for r, c in tile_coords:
        abs_r = r + start_r
        abs_c = c + start_c

        # Check bounds
        if abs_r < 0 or abs_r >= grid_height or abs_c < 0 or abs_c >= grid_width:
            return False

        # Check conflicts with already occupied positions
        if (abs_r, abs_c) in occupied:
            return False

    return True

def solve(grid_width: int, grid_height: int, tiles_to_place: List[int],
          all_orientations: dict[int, List[Set[Tuple[int, int]]]]) -> bool:
    """
    Use backtracking to determine if all tiles can be placed in the grid.

    Returns True if at least one valid arrangement exists.
    """
    # Early check: can the grid even hold all the filled cells?
    total_filled = sum(len(all_orientations[tid][0]) for tid in tiles_to_place)
    if total_filled > grid_width * grid_height:
        return False

    # Sort tiles by number of orientations (most constrained first) - do once at start
    tiles_to_place_sorted = sorted(tiles_to_place, key=lambda tid: len(all_orientations[tid]))

    def backtrack(tile_index: int, occupied: Set[Tuple[int, int]]) -> bool:
        # All tiles placed successfully
        if tile_index == len(tiles_to_place_sorted):
            return True

        tile_id = tiles_to_place_sorted[tile_index]

        # Try each orientation of the current tile
        for orientation in all_orientations[tile_id]:
            tile_height, tile_width = get_bounds(orientation)

            # Try each position in the grid
            # Limit search space based on tile bounds
            for start_r in range(max(0, grid_height - tile_height + 1)):
                for start_c in range(max(0, grid_width - tile_width + 1)):
                    if can_fit(grid_width, grid_height, orientation, start_r, start_c, occupied):
                        # Place tile
                        new_positions = place_tile(orientation, start_r, start_c)
                        new_occupied = occupied | new_positions

                        # Recurse
                        if backtrack(tile_index + 1, new_occupied):
                            return True

        return False

    return backtrack(0, set())

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "input"
    global DEBUG
    DEBUG = "--debug" in sys.argv

    tiles, test_cases = parse_input(filename)

    debug(f"Parsed {len(tiles)} tiles")
    for tile_id, coords in tiles.items():
        debug(f"  Tile {tile_id}: {len(coords)} filled positions")

    # Pre-generate all orientations for each tile
    all_orientations = {}
    for tile_id, coords in tiles.items():
        orientations = generate_orientations(coords)
        all_orientations[tile_id] = orientations
        debug(f"  Tile {tile_id}: {len(orientations)} unique orientations")

    debug(f"\nProcessing {len(test_cases)} test cases...")

    part1_count = 0

    for i, (width, height, counts) in enumerate(test_cases):
        # Build list of tiles to place
        tiles_to_place = []
        for tile_id, count in enumerate(counts):
            tiles_to_place.extend([tile_id] * count)

        debug(f"\nTest case {i+1}: {width}x{height} grid, tiles: {tiles_to_place}")

        if solve(width, height, tiles_to_place, all_orientations):
            debug(f"  ✓ Can fit!")
            part1_count += 1
        else:
            debug(f"  ✗ Cannot fit")

    print(f"Part 1: {part1_count}")

if __name__ == "__main__":
    main()
