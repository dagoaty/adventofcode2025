# Advent of Code 2025 - Project Context

## Project Overview

This repository contains Python solutions for Advent of Code 2025 challenges. Each day's challenge is organized in its own directory with a standalone Python solution.

## File Organization Pattern

- **Each day**: Separate directory named `dayN/` where N is the day number
- **Solution file**: `solution.py` - executable Python script with shebang (`#!/usr/bin/env python3`)
- **Input files**: `input` and `input.test` files are gitignored (per `.gitignore`)
- **Running**: `python3 dayN/solution.py [filename] [--debug]`

## Code Conventions

### Structure
Each solution is self-contained in a single `solution.py` file with no shared utility modules. Standard structure:
- Input parsing function
- Core algorithm functions for Part 1 and Part 2
- `main()` function orchestrates: parse → solve part 1 → solve part 2 → display results
- Argument parsing supporting custom input files and `--debug` flag
- `if __name__ == "__main__"` guard

Additional requirements:
- Solutions should complete in under 4 seconds
- All solutions run both Part 1 and Part 2, displaying results together
- Refactor working solutions to improve maintainability (extract common logic, eliminate duplication, improve naming)

### Style
- Python 3 with type hints on function signatures (e.g., `def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:`)
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

#### Day 5
- **Problem**: Range coverage analysis with numerical ranges
- **Part 1**: Count how many integers from a given list appear in any range
- **Part 2**: Count total number of distinct integers covered by all ranges
- **Algorithm**: O(m log m) for sorting + O(m) for merging ranges + O(n × m') for Part 1 checking, where m = number of ranges, m' = merged ranges, n = numbers to check
- **Features**: Merges overlapping and adjacent ranges for efficiency; ranges are inclusive on both ends [start, end]
- **Key functions**: `merge_ranges()`, `is_in_any_range()`, `count_numbers_in_ranges()`, `count_total_integers_in_ranges()`
- **Refactoring applied**: Eliminated redundant merge operations by merging once in main(); extracted Part 2 logic into dedicated function for consistency with Part 1
- **Note**: Adjacent ranges (e.g., [3,5] and [6,8]) are merged into single ranges for optimal performance

#### Day 7
- **Problem**: Line splitting simulation on a grid (lines travel south, split when hitting '^' symbols)
- **Part 1**: Lines merge when reaching same position; count total number of splits
- **Part 2**: No merging (universe splits into parallel realities); count total distinct line paths
- **Algorithm**: Row-by-row simulation - O(rows × active_columns) for both parts
- **Features**: Part 1 uses set (merging); Part 2 uses dictionary to track line multiplicities (avoids exponential space from grid copying)
- **Key functions**: `get_split_positions()`, `simulate_line_splits()`, `count_line_paths()`
- **Refactoring applied**: Extracted `get_split_positions()` helper to eliminate duplicated bounds-checking logic between Part 1 and Part 2
- **Note**: When line at (row, col) hits '^', it splits into two lines at (row, col-1) and (row, col+1) that continue south

#### Day 8
- **Problem**: Shortest distance clustering in 3D space with Union-Find
- **Part 1**: Connect n shortest pairs of 3D coordinates; return product of 3 largest connected component sizes
- **Part 2**: Connect pairs sequentially until all coordinates form single component; return product of x-coordinates of unifying pair
- **Algorithm**: O(N² log N) for calculating and sorting all pairwise distances; O(N × α(N)) for Union-Find operations where α is inverse Ackermann (effectively constant)
- **Features**: Union-Find with path compression and union by rank; component count tracking; shared distance calculations between parts
- **Key functions**: `UnionFind` class with `find()`, `union()`, `get_component_sizes()`; `calculate_all_distances()`; `solve_part1()`, `solve_part2()`
- **Type aliases**: `Coordinate = Tuple[int, int, int]` and `DistancePair = Tuple[float, int, int]` for improved readability
- **Refactoring applied**:
  - Extracted `get_component_sizes()` method into UnionFind class to encapsulate component counting logic
  - Extracted `determine_part1_connections()` helper for input-size-to-connections mapping
  - Added type aliases to simplify complex nested type signatures
  - Enhanced UnionFind documentation with comprehensive Attributes section
- **Note**: Part 2 expected complexity is O(N log N) for random spatial data; worst case O(N²) runs in ~0.35s for N=1000

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
2. Create `solution.py` following the structure conventions above
3. Test with `input.test` for example cases before running on `input` for actual puzzle input
4. Ensure solution completes in under 4 seconds
5. Refactor if needed to improve maintainability
