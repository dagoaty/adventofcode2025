#!/usr/bin/env python3
"""
Day 8: Shortest Distance Clustering

Part 1: Connect n shortest pairs, find product of 3 largest component sizes.
Part 2: Connect pairs until all coordinates form single set, return product of
        x-coordinates of the final unifying pair.
"""

import sys
import math
from typing import List, Tuple

# Type aliases for clarity
Coordinate = Tuple[int, int, int]  # (x, y, z)
DistancePair = Tuple[float, int, int]  # (distance, index1, index2)


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure with path compression and union by rank.

    Efficiently tracks connected components as we union points together. Maintains a count
    of connected components for quick queries about connectivity status.

    Attributes:
        parent: List mapping each element to its parent in the union-find tree
        rank: List of ranks for union by rank optimization
        component_count: Current number of distinct connected components
    """

    def __init__(self, size: int):
        """
        Initialize Union-Find structure with size elements.

        Args:
            size: Number of elements (coordinates)
        """
        self.parent = list(range(size))  # Each element is its own parent initially
        self.rank = [0] * size  # Rank for union by rank optimization
        self.component_count = size  # Initially, each element is its own component

    def find(self, x: int) -> int:
        """
        Find the root representative of element x with path compression.

        Args:
            x: Element index

        Returns:
            Root representative of x's set
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union the sets containing x and y using union by rank.

        Args:
            x: First element index
            y: Second element index

        Returns:
            True if union occurred (sets were different), False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union by rank: attach smaller tree to larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        # Decrement component count after successful union
        self.component_count -= 1
        return True

    def get_component_sizes(self) -> List[int]:
        """
        Get the sizes of all connected components.

        Returns:
            List of component sizes (one per component)
        """
        size_map = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            size_map[root] = size_map.get(root, 0) + 1
        return list(size_map.values())


def parse_coordinates(filename: str) -> List[Coordinate]:
    """
    Parse 3D coordinates from input file.

    Args:
        filename: Path to input file

    Returns:
        List of (x, y, z) coordinate tuples
    """
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
            coordinates.append((x, y, z))
    return coordinates


def calculate_distance(coord1: Coordinate, coord2: Coordinate) -> float:
    """
    Calculate Euclidean distance between two 3D points.

    Args:
        coord1: First coordinate (x, y, z)
        coord2: Second coordinate (x, y, z)

    Returns:
        Euclidean distance
    """
    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]
    dz = coord2[2] - coord1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def calculate_all_distances(coordinates: List[Coordinate]) -> List[DistancePair]:
    """
    Calculate distances between all pairs of coordinates.

    Args:
        coordinates: List of (x, y, z) tuples

    Returns:
        List of (distance, index1, index2) tuples for all pairs
    """
    distances = []
    n = len(coordinates)

    for i in range(n):
        for j in range(i + 1, n):
            dist = calculate_distance(coordinates[i], coordinates[j])
            distances.append((dist, i, j))

    return distances


def determine_part1_connections(num_coords: int) -> int:
    """
    Determine the number of connections to make for Part 1 based on input size.

    Args:
        num_coords: Number of coordinates in the input

    Returns:
        Number of connections to make for Part 1
    """
    if num_coords == 20:
        return 10  # Test input
    elif num_coords == 1000:
        return 1000  # Main input
    else:
        # Default: use half the number of coordinates
        return num_coords // 2


def solve_part1(coordinates: List[Coordinate], sorted_distances: List[DistancePair],
                n_connections: int, debug: bool = False) -> int:
    """
    Part 1: Connect n shortest pairs and find product of 3 largest components.

    Args:
        coordinates: List of (x, y, z) coordinate tuples
        sorted_distances: List of (distance, index1, index2) tuples, sorted by distance
        n_connections: Number of shortest connections to make
        debug: Whether to print debug information

    Returns:
        Product of the 3 largest component sizes
    """
    num_coords = len(coordinates)

    if debug:
        print(f"\n=== Part 1 ===")
        print(f"Taking {n_connections} shortest connections...")
        print(f"Shortest distance: {sorted_distances[0][0]:.2f}")
        print(f"Connection #{n_connections} distance: {sorted_distances[n_connections-1][0]:.2f}")

    # Initialize Union-Find
    uf = UnionFind(num_coords)

    # Connect the n shortest pairs
    for i in range(n_connections):
        _, idx1, idx2 = sorted_distances[i]
        uf.union(idx1, idx2)

    # Get component sizes and sort descending
    sizes = sorted(uf.get_component_sizes(), reverse=True)

    if debug:
        print(f"\nNumber of components: {len(sizes)}")
        print(f"Component sizes (sorted): {sizes[:10]}")  # Show top 10
        print(f"Three largest: {sizes[0]}, {sizes[1]}, {sizes[2]}")

    # Return product of 3 largest
    return sizes[0] * sizes[1] * sizes[2]


def solve_part2(coordinates: List[Coordinate], sorted_distances: List[DistancePair],
                debug: bool = False) -> int:
    """
    Part 2: Connect pairs until all coordinates form a single set, return product of
            x-coordinates of the final unifying pair.

    Args:
        coordinates: List of (x, y, z) coordinate tuples
        sorted_distances: List of (distance, index1, index2) tuples, sorted by distance
        debug: Whether to print debug information

    Returns:
        Product of x-coordinates of the pair that unified all components
    """
    num_coords = len(coordinates)

    if debug:
        print(f"\n=== Part 2 ===")
        print(f"Connecting pairs until single component forms...")

    # Initialize Union-Find
    uf = UnionFind(num_coords)

    # Process connections in order until we have a single component
    for i, (dist, idx1, idx2) in enumerate(sorted_distances):
        # Check if this union actually merges two different sets
        unified = uf.union(idx1, idx2)

        if unified and uf.component_count == 1:
            # This connection unified all coordinates into single set
            x1, x2 = coordinates[idx1][0], coordinates[idx2][0]
            result = x1 * x2

            if debug:
                print(f"Unified at connection #{i+1} (distance: {dist:.2f})")
                print(f"Points: index {idx1} ({coordinates[idx1]}) and index {idx2} ({coordinates[idx2]})")
                print(f"x-coordinates: {x1} * {x2} = {result}")

            return result

    # Should never reach here if input is valid
    raise ValueError("Failed to unify all coordinates into single component")


def main():
    """Main entry point for the solution."""
    # Parse command-line arguments
    filename = "input"
    debug = False

    for arg in sys.argv[1:]:
        if arg == "--debug":
            debug = True
        else:
            filename = arg

    # Parse coordinates
    coordinates = parse_coordinates(filename)

    # Determine number of connections for Part 1
    n_connections = determine_part1_connections(len(coordinates))

    if debug:
        print(f"Input: {filename}")
        print(f"Coordinates: {len(coordinates)}")
        print(f"Part 1 connections: {n_connections}")

    # Calculate all pairwise distances (shared between both parts)
    if debug:
        print(f"\nCalculating all pairwise distances...")

    sorted_distances = calculate_all_distances(coordinates)

    if debug:
        print(f"Total pairs: {len(sorted_distances)}")
        print(f"Sorting distances...")

    # Sort by distance (ascending)
    sorted_distances.sort(key=lambda x: x[0])

    # Solve Part 1
    part1_result = solve_part1(coordinates, sorted_distances, n_connections, debug)

    # Solve Part 2
    part2_result = solve_part2(coordinates, sorted_distances, debug)

    # Display results
    print(f"\nPart 1: {part1_result}")
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
