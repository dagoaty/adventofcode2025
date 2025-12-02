# Advent of Code 2025 - Project Context

## Project Overview

This repository contains Python solutions for Advent of Code 2025 challenges. Each day's challenge is organized in its own directory with a standalone Python solution.

## Repository Structure

```
adventofcode2025/
├── day1/
│   └── solution.py
├── day2/
│   └── solution.py
├── .gitignore
└── README.md
```

## File Organization Pattern

- **Each day**: Separate directory named `dayN/` where N is the day number
- **Solution file**: `solution.py` - executable Python script with shebang (`#!/usr/bin/env python3`)
- **Input files**: `input` and `input.test` files are gitignored (per `.gitignore`)

## Running Solutions

Solutions follow a consistent pattern:

```bash
# Run with default input file named "input"
python3 dayN/solution.py

# Run with custom input file
python3 dayN/solution.py <filename>

# Run with debug output
python3 dayN/solution.py --debug
python3 dayN/solution.py <filename> --debug
```

All solutions can be executed directly due to shebang and `if __name__ == "__main__"` guard.

## Code Conventions

### Structure
- Each solution is self-contained in a single `solution.py` file
- Solutions have a `main()` function that handles argument parsing
- Helper functions with docstrings for complex logic
- Debug mode support via `--debug` flag

### Style
- Python 3 with type hints in docstrings
- Clear function documentation explaining parameters and returns
- Meaningful variable names and constants (e.g., `DIAL_SIZE`, `STARTING_POSITION`)
- Comprehensive comments for non-obvious logic

### Day-Specific Notes

#### Day 1
- **Problem**: Dial rotation simulation (100-position circular dial)
- **Features**: Tracks zero crossings (stops and pass-throughs)
- **Key functions**: `count_zero_crossings()`, `apply_rotation()`, `process_instructions()`

#### Day 2
- **Problem**: Pattern repetition detection in numbers
- **Features**: Two-part solution checking different pattern repetition criteria
- **Key functions**: `get_pattern_repetitions()`, `has_any_pattern_repeating_twice()`, `process_ranges()`

## Git Workflow

- **Main branch**: Default branch for stable solutions
- **Feature branches**: Named with pattern `claude/*` for development
- Input files are gitignored to avoid committing puzzle inputs

## Development Guidelines

When adding new day solutions:

1. Create new directory: `dayN/`
2. Create `solution.py` with:
   - Shebang line: `#!/usr/bin/env python3`
   - Helper functions with docstrings
   - `main()` function with argument parsing
   - Support for custom input files and `--debug` flag
   - `if __name__ == "__main__"` guard
3. Test with example input before running on actual input
4. Keep input files local (they're gitignored)

## Testing Approach

- Use `input.test` files for example/test cases (gitignored)
- Use `input` files for actual puzzle input (gitignored)
- Debug mode prints step-by-step execution for verification

## Notes

- Solutions are written for clarity and correctness, not performance optimization
- Each solution is independent - no shared utility modules
- Puzzle inputs are user-specific and should not be committed to the repository
