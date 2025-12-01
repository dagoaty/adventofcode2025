#!/usr/bin/env python3

DIAL_SIZE = 100
STARTING_POSITION = 50


def count_zero_crossings(start_pos, amount, is_decrease):
    """
    Calculate how many times the dial passes through 0 during a rotation.

    Args:
        start_pos: Starting position (0-99)
        amount: Amount to rotate
        is_decrease: True if decreasing (L), False if increasing (R)

    Returns:
        Number of times the dial crosses 0
    """
    if start_pos == 0:
        # Starting at 0, we hit it again every 100 positions
        return amount // DIAL_SIZE if amount >= DIAL_SIZE else 0

    if is_decrease:
        # Decreasing: hit 0 at start_pos, start_pos+100, start_pos+200, ...
        return 1 + (amount - start_pos) // DIAL_SIZE if amount >= start_pos else 0
    else:
        # Increasing: hit 0 at (100-start_pos), (100-start_pos)+100, ...
        distance_to_zero = DIAL_SIZE - start_pos
        return 1 + (amount - distance_to_zero) // DIAL_SIZE if amount >= distance_to_zero else 0


def apply_rotation(position, amount, is_decrease):
    """Apply a rotation and return the new position."""
    if is_decrease:
        return (position - amount) % DIAL_SIZE
    else:
        return (position + amount) % DIAL_SIZE


def log_debug(instruction, amount, old_pos, new_pos, times_hit, times_passed):
    """Print debug information about a rotation."""
    if times_passed > 0:
        print(f"PASS_THROUGH x{times_passed}: {instruction}{amount}: {old_pos} -> {new_pos} (hits_zero={times_hit})")
    elif times_hit > 0:
        print(f"NO_PASS: {instruction}{amount}: {old_pos} -> {new_pos} (hits_zero={times_hit}, stops_on_0)")
    else:
        print(f"NO_WRAP: {instruction}{amount}: {old_pos} -> {new_pos}")


def process_instructions(filename, debug=False):
    """
    Process dial rotation instructions and track zero crossings.

    Args:
        filename: Path to input file with instructions
        debug: If True, print debug information

    Returns:
        tuple: (final_position, stops_on_zero, passes_through_zero)
    """
    position = STARTING_POSITION
    stops_on_zero = 0
    passes_through_zero = 0

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Parse instruction: first char is L/R, rest is amount
            instruction = line[0]
            amount = int(line[1:])

            if instruction not in ('L', 'R'):
                raise ValueError(f"Unknown instruction: {instruction}")

            # Calculate rotation
            is_decrease = (instruction == 'L')
            old_position = position
            position = apply_rotation(position, amount, is_decrease)

            # Count zero crossings
            times_hit_zero = count_zero_crossings(old_position, amount, is_decrease)
            stopped_on_zero = (position == 0)
            times_passed_through = times_hit_zero - (1 if stopped_on_zero else 0)

            # Update counters
            passes_through_zero += times_passed_through
            if stopped_on_zero:
                stops_on_zero += 1

            # Debug output
            if debug:
                log_debug(instruction, amount, old_position, position,
                         times_hit_zero, times_passed_through)
                if stopped_on_zero:
                    print(f"  -> STOP_ON_0 (total stops: {stops_on_zero})")

    return position, stops_on_zero, passes_through_zero


def main():
    """Parse arguments and run the solution."""
    import sys

    debug = "--debug" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--debug"]
    filename = args[0] if args else "input"

    final_pos, stops, passes = process_instructions(filename, debug=debug)

    print(f"\nFinal holding variable value: {final_pos}")
    print(f"Number of times variable was 0: {stops}")
    print(f"Number of times variable passed through 0: {passes}")
    print(f"Total (stops + pass-throughs): {stops + passes}")


if __name__ == "__main__":
    main()
