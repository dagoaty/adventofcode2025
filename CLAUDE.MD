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
├── day3/
│   └── solution.py
├── day4/
│   └── solution.py
├── .gitignore
├── CLAUDE.md
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
- All solutions run both Part 1 and Part 2, displaying results together
- Solutions should complete in under 4 seconds
- Refactor working solutions to improve maintainability (extract common logic, eliminate duplication, improve naming)

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

#### Day 3
- **Problem**: Maximum digit selection from lines of digits
- **Part 1**: Select 2 digits to form the largest possible two-digit number
- **Part 2**: Select 12 digits to form the largest possible 12-digit number
- **Algorithm**: Part 1 uses O(n) right-to-left scan; Part 2 uses O(n) greedy algorithm
- **Features**: Both parts run automatically in single execution
- **Key functions**: `find_max_two_digit()`, `find_max_k_digit()`
- **Note**: Digits must maintain their original order but can be non-consecutive

#### Day 4
- **Problem**: Grid neighbor analysis with @ and . symbols
- **Part 1**: Count @ symbols with fewer than 4 @ neighbors in 8 directions (N, NE, E, SE, S, SW, W, NW)
- **Part 2**: Iteratively remove @ symbols with < 4 neighbors until grid stabilizes
- **Algorithm**: O(m × n) per grid scan; Part 2 is O(L × m × n) where L = number of removal iterations
- **Features**: Two-phase per iteration (identify all candidates, then remove simultaneously)
- **Key functions**: `count_neighbors()`, `find_symbols_with_few_neighbors()`, `count_isolated_at_symbols()`, `iterative_removal()`
- **Refactoring applied**: Extracted common grid-scanning logic into `find_symbols_with_few_neighbors()` helper to eliminate duplication between Part 1 and Part 2
- **Note**: Neighbor threshold is < 4 (strictly less than, not ≤ 4) for both parts

## Git Workflow

- **Main branch**: Default branch for stable solutions
- **Feature branches**: Named with pattern `claude/*` for development
- Input files are gitignored to avoid committing puzzle inputs

## Development Guidelines

### Outline Before Implementation

**CRITICAL WORKFLOW REQUIREMENT**: Always outline solutions, algorithms, and refactorings BEFORE implementing them.

#### For New Solutions:
1. **Describe the algorithm**: Explain the approach in plain language
2. **Provide examples**: Walk through how it works on sample data
3. **Analyze complexity**: State time and space complexity (Big O notation)
4. **Identify edge cases**: Note boundary conditions and special cases
5. **Wait for approval**: Do not write code until the outline is reviewed

#### For Refactoring:
1. **Identify improvements**: Explain what will be better (DRY, readability, performance, maintainability)
2. **Show scope**: List which functions/sections will be modified
3. **Describe changes**: Explain the specific refactoring techniques (extract function, rename, etc.)
4. **Note risks**: Mention any potential side effects or behavior changes
5. **Wait for approval**: Do not modify working code until the outline is reviewed

#### For Bug Fixes:
1. **Explain root cause**: Describe what's wrong and why
2. **Outline the fix**: Describe the solution approach
3. **Note side effects**: Mention any other code that might be affected

**Rationale**: Outlining ensures alignment on approach, enables early feedback, catches design issues before implementation, and respects the collaborative nature of problem-solving.

### Adding New Day Solutions

When adding new day solutions:

1. Create new directory: `dayN/`
2. Create `solution.py` with:
   - Shebang line: `#!/usr/bin/env python3`
   - Helper functions with docstrings for both Part 1 and Part 2
   - `main()` function that runs both parts and displays results separately
   - Argument parsing supporting custom input files and `--debug` flag
   - `if __name__ == "__main__"` guard
   - Efficient algorithms ensuring completion within 4 seconds
3. Test with example input before running on actual input
4. Keep input files local (they're gitignored)

## Testing Approach

- Use `input.test` files for example/test cases (gitignored)
- Use `input` files for actual puzzle input (gitignored)
- Debug mode prints step-by-step execution for verification

## Notes

- Solutions prioritize clarity and correctness while maintaining efficiency (target: <4 seconds runtime)
- Each solution is independent - no shared utility modules
- Puzzle inputs are user-specific and should not be committed to the repository
- All problems contain two parts - solutions run both parts in a single execution for efficiency
- Both part results are calculated and displayed together
