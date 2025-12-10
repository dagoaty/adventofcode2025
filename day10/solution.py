#!/usr/bin/env python3

from collections import deque
import sys
import re
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np


# Type alias for parsed row data
Row = tuple[int, int, list[int], list[list[int]], list[int]]


def parse_input(filename: str) -> list[Row]:
    """
    Parse input file into list of row data.

    Each line format: [.##.] (3) (1,3) (2) ... {numbers}
    - Square brackets contain target binary string (. = 0, # = 1)
    - Parentheses contain flip operations (0-indexed positions)
    - Curly braces contain target flip counts per bit position

    Returns:
        List of tuples: (target_binary, bit_length, operation_bitmasks,
                        operation_arrays, flip_targets)
    """
    rows = []

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Extract target binary string from square brackets
            binary_match = re.search(r'\[([.#]+)\]', line)
            if not binary_match:
                continue

            binary_str = binary_match.group(1)
            bit_length = len(binary_str)

            # Convert binary string to integer: . = 0, # = 1
            target = int(binary_str.replace('.', '0').replace('#', '1'), 2)

            # Extract all operations from parentheses
            operations = []
            operation_arrays = []

            for op_match in re.finditer(r'\(([0-9,]+)\)', line):
                positions = [int(p) for p in op_match.group(1).split(',')]

                # Build bitmask for Part 1 (bit position 0 is leftmost)
                bitmask = 0
                for pos in positions:
                    bitmask |= (1 << (bit_length - 1 - pos))
                operations.append(bitmask)

                # Build array for Part 2 (array index matches bit position)
                op_array = [0] * bit_length
                for pos in positions:
                    op_array[pos] = 1
                operation_arrays.append(op_array)

            # Extract flip targets from curly braces
            flip_targets = []
            braces_match = re.search(r'\{([0-9,]+)\}', line)
            if braces_match:
                flip_targets = [int(n) for n in braces_match.group(1).split(',')]

            rows.append((target, bit_length, operations, operation_arrays, flip_targets))

    return rows


def min_flips_bfs(target: int, operations: list[int]) -> int:
    """
    Find minimum operations to reach target binary state from 0 using BFS.

    Args:
        target: Target binary value as integer
        operations: List of operation bitmasks to XOR with current state

    Returns:
        Minimum number of operations needed
    """
    if target == 0:
        return 0

    queue = deque([(0, 0)])  # (current_state, num_operations)
    visited = {0}

    while queue:
        current_state, num_ops = queue.popleft()

        # Try all operations
        for operation in operations:
            new_state = current_state ^ operation

            # Check if we reached the target
            if new_state == target:
                return num_ops + 1

            # Add to queue if not visited
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, num_ops + 1))

    # Target unreachable
    return -1


def min_flips_milp(flip_targets: list[int], operation_arrays: list[list[int]]) -> int:
    """
    Find minimum operations to achieve exact flip counts using MILP solver.

    Formulates the problem as:
        minimize: sum(x)
        subject to: A × x = b, x >= 0, x integer

    Where:
        A[i][j] = 1 if operation j flips bit i, else 0
        x[j] = number of times to use operation j (decision variable)
        b[i] = target flip count for bit i

    Args:
        flip_targets: Target number of flips for each bit position
        operation_arrays: List of binary arrays showing which bits each operation flips

    Returns:
        Minimum total number of operations needed
    """
    num_bits = len(flip_targets)
    num_ops = len(operation_arrays)

    # Build constraint matrix: rows=bits, columns=operations
    # A[i][j] = 1 if operation j affects bit i
    A = np.array([[op[i] for op in operation_arrays] for i in range(num_bits)])

    # Equality constraints: each bit must be flipped exactly flip_targets[i] times
    constraints = LinearConstraint(A, lb=flip_targets, ub=flip_targets)

    # Objective: minimize total number of operations
    c = np.ones(num_ops)

    # Variable bounds: all operation counts must be non-negative
    bounds = Bounds(lb=0, ub=np.inf)

    # Integer constraints: all variables must be integers
    integrality = np.ones(num_ops)

    # Solve MILP
    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(result.fun))
    else:
        # This shouldn't happen with valid inputs
        raise RuntimeError(f"MILP solver failed: {result.message}")


def solve_part1(rows: list[Row]) -> int:
    """
    Solve Part 1: Sum of minimum flips for all rows.

    Args:
        rows: Parsed input data

    Returns:
        Sum of minimum flips across all rows
    """
    total = 0
    for target, _bit_length, operations, _operation_arrays, _flip_targets in rows:
        min_ops = min_flips_bfs(target, operations)
        total += min_ops

    return total


def solve_part2(rows: list[Row]) -> int:
    """
    Solve Part 2: Sum of minimum operations to achieve exact flip counts.

    Args:
        rows: Parsed input data

    Returns:
        Sum of minimum operations across all rows
    """
    total = 0
    for _target, _bit_length, _operations, operation_arrays, flip_targets in rows:
        min_ops = min_flips_milp(flip_targets, operation_arrays)
        total += min_ops

    return total


def main():
    # Parse command line arguments
    filename = "day10/input.test"
    debug = False

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--debug":
        debug = True

    # Parse input
    rows = parse_input(filename)

    if debug:
        print(f"Parsed {len(rows)} rows")
        for i, (target, bit_length, operations, _operation_arrays, flip_targets) in enumerate(rows, 1):
            print(f"Row {i}: target={bin(target)} ({target}), bits={bit_length}, ops={len(operations)}, flip_targets={flip_targets}")

    # Solve Part 1
    part1_result = solve_part1(rows)
    print(f"Part 1: {part1_result}")

    # Solve Part 2
    part2_result = solve_part2(rows)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
