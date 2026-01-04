import os
from typing import Optional, List, Set, Tuple

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

TARGET_CHAR = '@'

# --- Utility Functions ---

def get_lines_from_file(file_path: str) -> Optional[List[str]]:
    """Reads non-empty, stripped lines from the specified file."""
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def count_neighbors(grid: List[str], r: int, c: int, target: str) -> int:
    """
    Counts the number of TARGET_CHAR in the 3x3 neighborhood centered at (r, c),
    including the cell (r, c) itself. Handles boundary conditions.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    neighbor_count = 0

    # Iterate over the 3x3 neighborhood
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            nr, nc = r + dr, c + dc

            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == target:
                    neighbor_count += 1
                    
    return neighbor_count

# --- Part 1 Logic ---

def part1():
    """
    Finds the number of '@' characters whose 3x3 neighborhood contains 4 or fewer '@' characters (including itself).
    """
    grid = get_lines_from_file(FILE_PATH)
    if grid is None or not grid:
        return

    valid_indices: List[Tuple[int, int]] = []

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == TARGET_CHAR:
                # Count neighbors including the current cell
                count = count_neighbors(grid, r, c, TARGET_CHAR)
                
                # Check the condition: 4 or fewer '@' in the 3x3 neighborhood
                if count <= 4:
                    valid_indices.append((r, c))

    print(f"Part 1 answer: {len(valid_indices)}")

# --- Part 2 Logic ---

def part2():
    """
    Simulates a process where '@' characters become 'valid' if their neighborhood
    has 4 or fewer '@' characters *excluding* those already determined to be valid
    in a previous state. The process stabilizes when no new valid indices are found.
    """
    grid = get_lines_from_file(FILE_PATH)
    if grid is None or not grid:
        return

    # Use a set to track indices that have been determined to be "valid"
    valid_indices: Set[Tuple[int, int]] = set()
    
    # Store the maximum size reached for the final answer
    max_valid_count = 0
    
    # Grid dimensions
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # The simulation loop continues until the set of valid indices stabilizes (no new additions)
    while True:
        # A temporary set to store the candidates for the *next* state
        newly_valid_candidates: Set[Tuple[int, int]] = set()
        
        # Track if any new indices were added in this iteration
        new_indices_added = False

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == TARGET_CHAR and (r, c) not in valid_indices:
                    # Only consider '@' that are NOT already in the valid set

                    # Count neighbors, but *only* if they are NOT in the 'valid_indices' set
                    current_neighbor_count = 0
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc

                            if 0 <= nr < rows and 0 <= nc < cols:
                                if grid[nr][nc] == TARGET_CHAR:
                                    # Count only the '@' that are not yet considered 'valid'
                                    if (nr, nc) not in valid_indices:
                                        current_neighbor_count += 1
                    
                    # Check the condition: 4 or fewer UN-VALIDATED '@' in the 3x3 neighborhood
                    if current_neighbor_count <= 4:
                        newly_valid_candidates.add((r, c))

        # Check for convergence: if no new candidates were found
        if not newly_valid_candidates:
            break
        
        # Add all newly found candidates to the main set
        valid_indices.update(newly_valid_candidates)
        
        # Update the max count (though it only increases, so the final count is the max)
        max_valid_count = len(valid_indices)


    print(f"Part 2 answer: {len(valid_indices)}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()