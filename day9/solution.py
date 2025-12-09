#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9

Part 1: Find maximum area between coordinate pairs using (|x1-x2| + 1) × (|y1-y2| + 1)
Part 2: Find largest rectangle (corners from input) that fits inside polygon

Key optimization: Edge bucketing for point-in-polygon checks (16x speedup)
"""

import sys
from collections import defaultdict
from typing import DefaultDict, Iterator, List, Set, Tuple

Coordinate = Tuple[int, int]
Edge = Tuple[Coordinate, Coordinate]
RectangleBounds = Tuple[int, int, int, int]  # (min_x, max_x, min_y, max_y)


def get_rectangle_bounds(coord1: Coordinate, coord2: Coordinate) -> RectangleBounds:
    """
    Extract normalized bounds from two opposite corners of a rectangle.

    Args:
        coord1: First corner (x1, y1)
        coord2: Opposite corner (x2, y2)

    Returns:
        Tuple of (min_x, max_x, min_y, max_y)
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return (min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2))


def pairs(items: List[Coordinate]) -> Iterator[Tuple[Coordinate, Coordinate]]:
    """
    Generate all unique pairs from a list.

    Args:
        items: List of items to pair

    Yields:
        Tuples of (item_i, item_j) where i < j
    """
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            yield (items[i], items[j])


def parse_input(filename: str) -> List[Coordinate]:
    """
    Parse input file containing x,y coordinates (one per line).

    Args:
        filename: Path to input file

    Returns:
        List of (x, y) coordinate tuples
    """
    coordinates = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                coordinates.append((x, y))
    return coordinates


def calculate_area(coord1: Coordinate, coord2: Coordinate) -> int:
    """
    Calculate area between two coordinates using the formula:
    (|x1-x2| + 1) * (|y1-y2| + 1)

    Args:
        coord1: First coordinate (x1, y1)
        coord2: Second coordinate (x2, y2)

    Returns:
        Area value
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


# ============================================================================
# Part 1: Maximum area between any two coordinate pairs
# ============================================================================

def find_max_area(coordinates: List[Coordinate], debug: bool = False) -> int:
    """
    Find maximum area between any pair of coordinates using formula:
    (|x1-x2| + 1) * (|y1-y2| + 1)

    Algorithm: Check all pairs of coordinates in O(n²)
    Note: An optimization based on boundary points was attempted but proved
    incorrect - the maximum product doesn't necessarily come from maximizing
    individual factors, but from balanced factors.

    Args:
        coordinates: List of (x, y) coordinates
        debug: Whether to print debug information

    Returns:
        Maximum area value
    """
    max_area = 0
    best_pair = None

    for coord1, coord2 in pairs(coordinates):
        area = calculate_area(coord1, coord2)
        if area > max_area:
            max_area = area
            best_pair = (coord1, coord2)

    if debug and best_pair:
        print(f"Best pair: {best_pair[0]} and {best_pair[1]} with area {max_area}")

    return max_area


# ============================================================================
# Part 2: Largest rectangle inside polygon
# ============================================================================

def build_edge_buckets(polygon: List[Coordinate]) -> DefaultDict[int, List[Edge]]:
    """
    Build a spatial index of polygon edges bucketed by y-coordinate ranges.

    This allows point-in-polygon checks to only examine edges that could
    intersect a horizontal ray at a given y-coordinate, dramatically reducing
    the number of edges checked from O(n) to O(k) where k << n.

    Args:
        polygon: List of polygon vertices in order

    Returns:
        Dictionary mapping y-coordinate -> list of edges spanning that y
    """
    edge_buckets: DefaultDict[int, List[Edge]] = defaultdict(list)
    n = len(polygon)

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]
        edge = (p1, p2)

        # Get y-range this edge spans
        y1, y2 = p1[1], p2[1]
        min_y, max_y = min(y1, y2), max(y1, y2)

        # Add edge to all y-buckets it spans
        for y in range(min_y, max_y + 1):
            edge_buckets[y].append(edge)

    return edge_buckets


def point_in_polygon(point: Coordinate, edge_buckets: DefaultDict[int, List[Edge]]) -> bool:
    """
    Determine if a point is inside a polygon using ray casting algorithm.

    The algorithm casts a horizontal ray from the point to infinity and counts
    how many polygon edges it crosses. Odd count = inside, even count = outside.

    Performance: Uses edge bucketing to only check edges at the point's y-coordinate,
    reducing edge checks from O(n) to O(k) where k is typically 10-50 edges.

    Args:
        point: (x, y) coordinate to test
        edge_buckets: Pre-computed edge buckets indexed by y-coordinate

    Returns:
        True if point is inside or on the edge of polygon, False otherwise
    """
    x, y = point
    inside = False

    # Only check edges that could intersect a horizontal ray at this y-coordinate
    relevant_edges = edge_buckets.get(y, [])

    # Ray casting: count intersections with relevant polygon edges
    for edge in relevant_edges:
        (x1, y1), (x2, y2) = edge

        # Special case: point is on a horizontal edge of the polygon
        if y1 == y2 == y:
            if min(x1, x2) <= x <= max(x1, x2):
                return True

        # Special case: point is on a vertical edge of the polygon
        if x1 == x2 == x:
            if min(y1, y2) <= y <= max(y1, y2):
                return True

        # Normalize edge so y1 <= y2 (simplifies intersection logic)
        if y1 > y2:
            x1, y1, x2, y2 = x2, y2, x1, y1

        # Check if horizontal ray from point intersects this edge
        # Edge must span the ray's y-level: y1 <= y < y2
        # (using < for y2 avoids double-counting vertices)
        if y1 <= y < y2:
            # Calculate x-coordinate where edge crosses the ray's y-level
            # Using linear interpolation: x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

            # If intersection is to the right of or at the point, count it
            if x <= x_intersect:
                inside = not inside

    return inside


def get_rectangle_perimeter_test_points(
    min_x: int, max_x: int, min_y: int, max_y: int,
    polygon_x: List[int], polygon_y: List[int]
) -> Set[Coordinate]:
    """
    Get critical points to test on a rectangle's perimeter.

    For rectilinear polygons, testing at polygon vertex coordinates ensures
    we catch any polygon edges that might intersect the rectangle.

    Args:
        min_x, max_x: Rectangle x-bounds
        min_y, max_y: Rectangle y-bounds
        polygon_x: Sorted unique x-coordinates from polygon
        polygon_y: Sorted unique y-coordinates from polygon

    Returns:
        Set of points on rectangle perimeter to test
    """
    # Get x and y values within the rectangle range
    test_x = [min_x, max_x] + [x for x in polygon_x if min_x < x < max_x]
    test_y = [min_y, max_y] + [y for y in polygon_y if min_y < y < max_y]

    points_to_check = set()

    # Sample points along all four edges of the rectangle
    for x in test_x:
        points_to_check.add((x, min_y))  # Bottom edge
        points_to_check.add((x, max_y))  # Top edge

    for y in test_y:
        points_to_check.add((min_x, y))  # Left edge
        points_to_check.add((max_x, y))  # Right edge

    return points_to_check


def rectangle_inside_polygon(
    coord1: Coordinate, coord2: Coordinate,
    polygon_x: List[int], polygon_y: List[int],
    edge_buckets: DefaultDict[int, List[Edge]]
) -> bool:
    """
    Check if a rectangle defined by two opposite corners is entirely inside a polygon.

    For rectilinear polygons with potential concavities, we need to check more than
    just the corners. We sample points along the edges at all polygon vertex coordinates.

    Args:
        coord1: First corner of rectangle
        coord2: Opposite corner of rectangle
        polygon_x: Cached sorted unique x-coordinates from polygon
        polygon_y: Cached sorted unique y-coordinates from polygon
        edge_buckets: Pre-computed edge buckets for fast point-in-polygon checks

    Returns:
        True if rectangle is entirely inside polygon
    """
    min_x, max_x, min_y, max_y = get_rectangle_bounds(coord1, coord2)

    # Get critical test points on rectangle perimeter
    points_to_check = get_rectangle_perimeter_test_points(
        min_x, max_x, min_y, max_y, polygon_x, polygon_y
    )

    # Check all sampled points are inside polygon
    for point in points_to_check:
        if not point_in_polygon(point, edge_buckets):
            return False

    return True


def find_largest_rectangle_in_polygon(coordinates: List[Coordinate], debug: bool = False) -> int:
    """
    Find the largest rectangle (using inclusive area formula) with corners
    from the coordinate list that fits entirely inside the polygon.

    Algorithm:
    - Check all pairs of coordinates as potential rectangle corners
    - Verify rectangle is entirely inside polygon (requires sampling perimeter points)
    - Calculate area using (|x1-x2| + 1) * (|y1-y2| + 1)

    Performance optimizations:
    - Pre-computes polygon x/y coordinates to avoid repeated work
    - Uses edge bucketing to accelerate point-in-polygon checks from O(n) to O(k)

    Args:
        coordinates: Polygon vertices in order
        debug: Whether to print debug information

    Returns:
        Area of largest rectangle (using inclusive formula)
    """
    # Pre-compute polygon vertex coordinates (used for all rectangle checks)
    polygon_x = sorted(set(x for x, _ in coordinates))
    polygon_y = sorted(set(y for _, y in coordinates))

    # Build edge buckets for fast point-in-polygon checks
    edge_buckets = build_edge_buckets(coordinates)

    if debug:
        avg_edges = sum(len(edges) for edges in edge_buckets.values()) / len(edge_buckets)
        print(f"Edge bucketing: avg {avg_edges:.1f} edges per y-level (vs {len(coordinates)} total)")

    max_area = 0
    best_pair = None

    # Check all pairs of coordinates as potential rectangle corners
    for coord1, coord2 in pairs(coordinates):
        # Check if rectangle defined by these corners is inside polygon
        if rectangle_inside_polygon(coord1, coord2, polygon_x, polygon_y, edge_buckets):
            # Calculate area using inclusive formula (same as Part 1)
            area = calculate_area(coord1, coord2)

            if area > max_area:
                max_area = area
                best_pair = (coord1, coord2)

    if debug and best_pair:
        print(f"Largest rectangle: {best_pair[0]} to {best_pair[1]}")
        min_x, max_x, min_y, max_y = get_rectangle_bounds(best_pair[0], best_pair[1])
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        print(f"Dimensions: {width} × {height} = {max_area}")

    return max_area


def main():
    """Main execution function"""
    # Parse command line arguments
    filename = "input.test" if len(sys.argv) < 2 else sys.argv[1]
    debug = "--debug" in sys.argv

    # Parse input
    coordinates = parse_input(filename)

    if debug:
        print(f"Loaded {len(coordinates)} coordinates")
        print(f"Coordinates: {coordinates[:10]}{'...' if len(coordinates) > 10 else ''}")
        print()

    # Solve Part 1
    max_area = find_max_area(coordinates, debug)
    print(f"Part 1: Maximum area = {max_area}")

    # Solve Part 2
    if debug:
        print()
    max_rect_area = find_largest_rectangle_in_polygon(coordinates, debug)
    print(f"Part 2: Largest rectangle area = {max_rect_area}")


if __name__ == "__main__":
    main()
