#!/usr/bin/env python3


def get_pattern_repetitions(num):
    """
    Get the number of times the shortest pattern repeats in a number.

    Examples:
        11 -> 2 (pattern "1" repeated 2 times)
        111 -> 3 (pattern "1" repeated 3 times)
        1212 -> 2 (pattern "12" repeated 2 times)
        565656 -> 3 (pattern "56" repeated 3 times)
        123 -> 1 (no repeating pattern)
        111111 -> 6 (pattern "1" repeated 6 times, not "11" or "111")

    Args:
        num: Integer to check

    Returns:
        Number of times the shortest pattern repeats (1 if no pattern found)
    """
    s = str(num)
    n = len(s)

    # Try all possible pattern lengths from smallest to largest
    for pattern_len in range(1, n // 2 + 1):
        # Only check if pattern can evenly divide the string
        if n % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = n // pattern_len
            # Check if repeating the pattern forms the entire number
            if pattern * repetitions == s:
                return repetitions

    # No repeating pattern found
    return 1


def has_any_pattern_repeating_twice(num):
    """
    Check if there exists ANY pattern (not just shortest) that repeats exactly twice.

    Examples:
        222222 -> True (can be "222" repeated 2 times, even though shortest is "2" x 6)
        111111 -> True (can be "111" repeated 2 times)
        111 -> False (only "1" x 3, no pattern repeats exactly twice)
        1212 -> True ("12" repeated 2 times)

    Args:
        num: Integer to check

    Returns:
        True if any pattern repeats exactly twice, False otherwise
    """
    s = str(num)
    n = len(s)

    # Must be even length for any pattern to repeat exactly twice
    if n % 2 != 0:
        return False

    # Check if splitting in half gives two identical parts
    # This is equivalent to checking if SOME pattern repeats exactly twice
    half = n // 2
    return s[:half] == s[half:]


def process_ranges(filename, debug=False):
    """
    Process comma-separated ranges and sum invalid numbers for both parts.

    Args:
        filename: Path to input file with comma-separated ranges (format: start-end)
        debug: If True, print debug information

    Returns:
        Tuple of (part1_sum, part2_sum)
    """
    with open(filename, 'r') as f:
        data = f.read().strip()

    # Parse comma-separated ranges
    ranges = data.split(',')
    part1_total = 0
    part2_total = 0

    for range_str in ranges:
        start, end = map(int, range_str.split('-'))

        if debug:
            print(f"\nProcessing range {start}-{end}:")

        part1_sum = 0
        part2_sum = 0
        for num in range(start, end + 1):
            # Part 1: ANY pattern repeats exactly twice
            # Note: Part 1 is always a subset of Part 2, so we can optimize
            if has_any_pattern_repeating_twice(num):
                part1_sum += num
                part2_sum += num  # Always in Part 2 if in Part 1
                if debug:
                    print(f"  Part 1 & 2 - Found number with pattern x2: {num}")
            else:
                # Only check Part 2 if not already in Part 1
                reps = get_pattern_repetitions(num)
                if reps >= 2:
                    part2_sum += num
                    if debug:
                        print(f"  Part 2 only - Found number with pattern x{reps}: {num}")

        if debug:
            print(f"  Part 1 range sum: {part1_sum}")
            print(f"  Part 2 range sum: {part2_sum}")

        part1_total += part1_sum
        part2_total += part2_sum

    return part1_total, part2_total


def main():
    """Parse arguments and run the solution."""
    import sys

    debug = "--debug" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--debug"]
    filename = args[0] if args else "input"

    part1, part2 = process_ranges(filename, debug=debug)

    print(f"\nPart 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
