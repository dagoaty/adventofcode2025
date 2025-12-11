#!/usr/bin/env python3
"""
Day 11: Graph Path Counting

Count paths from 'you' to 'out' in a directed acyclic graph.
"""

import sys
from typing import Dict, List


def parse_input(filename: str) -> Dict[str, List[str]]:
    """
    Parse the input file into a graph adjacency list.

    Args:
        filename: Path to input file

    Returns:
        Dictionary mapping node name to list of connected nodes
    """
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse "node: neighbor1 neighbor2 ..."
            node, neighbors_str = line.split(': ')
            neighbors = neighbors_str.split()
            graph[node] = neighbors

    return graph


def count_paths(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count total number of paths from start node to end node.

    Uses memoization to efficiently count paths in a DAG.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node name
        end: Ending node name

    Returns:
        Total number of distinct paths from start to end
    """
    memo = {}

    def count_from(node: str) -> int:
        """Count paths from given node to end node."""
        # Base case: reached the end
        if node == end:
            return 1

        # Return cached result if available
        if node in memo:
            return memo[node]

        # Node not in graph or has no neighbors
        if node not in graph:
            return 0

        # Sum paths from all neighbors
        total = sum(count_from(neighbor) for neighbor in graph[node])

        memo[node] = total
        return total

    return count_from(start)


def count_paths_through_waypoints(graph: Dict[str, List[str]],
                                   start: str,
                                   waypoints: List[str],
                                   end: str) -> int:
    """
    Count paths from start to end passing through waypoints in order.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node name
        waypoints: List of intermediate nodes to pass through in order
        end: Ending node name

    Returns:
        Total number of paths from start to end through all waypoints
    """
    nodes = [start] + waypoints + [end]
    result = 1
    for i in range(len(nodes) - 1):
        result *= count_paths(graph, nodes[i], nodes[i + 1])
    return result


def solve_part1(graph: Dict[str, List[str]]) -> int:
    """
    Part 1: Count paths from 'you' to 'out'.

    Args:
        graph: The input graph

    Returns:
        Number of paths from 'you' to 'out'
    """
    return count_paths(graph, 'you', 'out')


def solve_part2(graph: Dict[str, List[str]]) -> int:
    """
    Part 2: Count paths from 'svr' to 'out' that pass through both 'dac' and 'fft'.

    The path must visit both intermediate nodes, but in either order:
    - svr → dac → fft → out
    - svr → fft → dac → out

    Args:
        graph: The input graph

    Returns:
        Number of paths from 'svr' to 'out' passing through both 'dac' and 'fft'
    """
    # Count paths for ordering: svr → dac → fft → out
    ordering1 = count_paths_through_waypoints(graph, 'svr', ['dac', 'fft'], 'out')

    # Count paths for ordering: svr → fft → dac → out
    ordering2 = count_paths_through_waypoints(graph, 'svr', ['fft', 'dac'], 'out')

    return ordering1 + ordering2


def main():
    """Main entry point."""
    # Parse command line arguments
    filename = 'day11/input'
    debug = False

    for arg in sys.argv[1:]:
        if arg == '--debug':
            debug = True
        else:
            filename = arg

    # Parse input
    graph = parse_input(filename)

    if debug:
        print(f"Graph: {graph}")

    # Solve parts
    part1 = solve_part1(graph)
    part2 = solve_part2(graph)

    # Display results
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
