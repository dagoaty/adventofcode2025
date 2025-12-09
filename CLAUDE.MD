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
- **Problem**: Dial rotation simulation (100-position circular dial, tracks zero crossings)
- **Algorithm**: O(n) single pass tracking position and crossings

#### Day 2
- **Problem**: Pattern repetition detection in numbers with different criteria for each part
- **Algorithm**: O(n × p) where n = number length, p = pattern lengths checked

#### Day 3
- **Problem**: Maximum digit selection from lines of digits
- **Part 1**: Select 2 digits to form largest two-digit number
- **Part 2**: Select 12 digits to form largest 12-digit number
- **Algorithm**: Part 1 uses O(n) right-to-left scan; Part 2 uses O(n) greedy algorithm
- **Note**: Digits must maintain original order but can be non-consecutive

#### Day 4
- **Problem**: Grid neighbor analysis - count/remove @ symbols based on neighbor count
- **Part 1**: Count @ symbols with < 4 @ neighbors (8 directions)
- **Part 2**: Iteratively remove @ symbols with < 4 neighbors until stable
- **Algorithm**: O(m × n) per scan; Part 2 is O(L × m × n) where L = iterations. Two-phase per iteration: identify candidates, then remove simultaneously to avoid order dependencies

#### Day 5
- **Problem**: Range coverage analysis
- **Part 1**: Count how many integers from a list appear in any range
- **Part 2**: Count total distinct integers covered by all ranges
- **Algorithm**: O(m log m) sort + O(m) merge + O(n × m') checking. Merges overlapping AND adjacent ranges (e.g., [3,5] and [6,8] → [3,8]) for efficiency
- **Note**: Ranges are inclusive [start, end]

#### Day 7
- **Problem**: Line splitting simulation (lines travel south, split on '^' symbols)
- **Part 1**: Lines merge at same position; count total splits
- **Part 2**: No merging (parallel universes); count distinct line paths
- **Algorithm**: Row-by-row O(rows × active_columns). Part 1 uses set (merging), Part 2 uses dictionary tracking multiplicities (avoids exponential space from grid copying)

#### Day 8
- **Problem**: 3D coordinate clustering using shortest distances
- **Part 1**: Connect n shortest pairs; return product of 3 largest component sizes
- **Part 2**: Connect pairs sequentially until single component; return product of unifying pair's x-coordinates
- **Algorithm**: O(N² log N) calculate/sort distances + O(N × α(N)) Union-Find (α ≈ constant). Union-Find uses path compression and union by rank
- **Note**: Part 2 expected O(N log N) for random data; worst O(N²) runs ~0.35s for N=1000

#### Day 9
- **Problem**: Rectangle area calculations
- **Part 1**: Find maximum area between any two coordinates using `(|x1-x2| + 1) × (|y1-y2| + 1)`
- **Part 2**: Find largest rectangle (corners from input) fitting inside rectilinear polygon
- **Algorithm**: Part 1 is O(n²) exhaustive search. Part 2 is O(n² × k × m) using edge bucketing (spatial index by y-coordinate) and ray casting for point-in-polygon, reducing m from ~496 to ~2 edges per point (16x speedup: 88s → 5.5s)
- **Note**: Part 1 boundary-point optimization failed - maximum product comes from balanced factors, not maximizing factors. Part 2 requires checking all four rectangle corners plus perimeter samples at polygon vertices (corner-only checking insufficient for concave polygons). Bounding box pre-filter was 0% effective when all coordinates on perimeter

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
