#!/usr/bin/env python3

import sys


def find_max_two_digit(line):
    """
    Find the highest two-digit number that can be formed from a line of digits.

    Numbers are formed by selecting two digits where the first comes before
    the second in position (but they don't need to be adjacent).

    Args:
        line: String of digits

    Returns:
        Integer representing the highest two-digit number possible
    """
    line = line.strip()

    if len(line) < 2:
        return 0

    max_value = 0
    max_right = int(line[-1])

    # Scan from right to left, tracking the maximum digit to the right
    for i in range(len(line) - 2, -1, -1):
        digit = int(line[i])
        # Form two-digit number with current digit and best digit to the right
        value = digit * 10 + max_right
        max_value = max(max_value, value)
        # Update the maximum digit seen so far
        max_right = max(max_right, digit)

    return max_value


def find_max_k_digit(line, k):
    """
    Find the highest k-digit number that can be formed from a line of digits.

    Uses a greedy algorithm: for each position in the result, select the
    largest available digit while ensuring enough digits remain for the rest.

    Args:
        line: String of digits
        k: Number of digits to select

    Returns:
        Integer representing the highest k-digit number possible
    """
    line = line.strip()
    n = len(line)

    if n < k:
        return 0

    result = []
    last_pos = -1

    # For each position in our k-digit result
    for i in range(k):
        # Calculate search range
        start = last_pos + 1
        end = n - (k - i) + 1  # Must leave enough digits for remaining positions

        # Find the maximum digit in the range
        # When there are ties, pick the leftmost to leave more digits for later
        max_digit = -1
        max_pos = start

        for j in range(start, end):
            digit = int(line[j])
            if digit > max_digit:  # > picks leftmost on ties
                max_digit = digit
                max_pos = j

        result.append(str(max_digit))
        last_pos = max_pos

    return int(''.join(result))


def main():
    # Parse arguments
    filename = "input"
    debug = False

    for arg in sys.argv[1:]:
        if arg == "--debug":
            debug = True
        elif not arg.startswith("-"):
            filename = arg

    # Read and process input
    part1_total = 0
    part2_total = 0

    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            part1_value = find_max_two_digit(line)
            part2_value = find_max_k_digit(line, 12)

            part1_total += part1_value
            part2_total += part2_value

            if debug:
                print(f"Line {line_num}: {line}")
                print(f"  Part 1: {part1_value}")
                print(f"  Part 2: {part2_value}")

    print(f"Part 1: {part1_total}")
    print(f"Part 2: {part2_total}")


if __name__ == "__main__":
    main()
