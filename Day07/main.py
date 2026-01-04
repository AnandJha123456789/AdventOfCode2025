import os
from typing import Optional, List, Set, Tuple, Dict, Any

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

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

# --- Core Logic ---

# A global (or context-passing) set is needed to track the side effect for Part 1
SplitterIndices = Set[Tuple[int, int]]

def beam_down(
    r: int, 
    c: int, 
    grid: List[List[str]], 
    memo: Dict[Tuple[int, int], int], 
    splitter_indices: SplitterIndices
) -> int:
    """
    Recursively calculates the number of "timelines" (paths) that can reach a cell.
    '^' characters split the path (1 path in -> 2 paths out).
    The function also tracks the indices of the '^' characters that were hit.
    """
    max_depth = len(grid)
    
    # Base Case 1: Reached the bottom of the grid successfully
    if r >= max_depth:
        return 1
    
    # Check boundaries horizontally (assuming the path stops if it goes out of bounds)
    max_width = len(grid[0]) if grid and grid[0] else 0
    if c < 0 or c >= max_width:
        return 0
        
    # Memoization check
    if (r, c) in memo:
        return memo[(r, c)]
    
    result = 0
    current_char = grid[r][c]
    
    if current_char == '^':
        # Part 1 logic: track the splitter index
        splitter_indices.add((r, c))
        
        # Split the beam: one path left, one path right (both at the current row)
        result = (
            beam_down(r, c - 1, grid, memo, splitter_indices) + 
            beam_down(r, c + 1, grid, memo, splitter_indices)
        )
    else:
        # Standard move: beam moves down to the next row
        result = beam_down(r + 1, c, grid, memo, splitter_indices)
    
    # Store and return the result
    memo[(r, c)] = result
    return result

def both():
    """
    Runs the simulation to find the number of unique splitter indices hit (Part 1)
    and the total number of new timelines/paths created (Part 2).
    """
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    # 1. Convert lines into a grid of characters
    grid: List[List[str]] = [list(line) for line in lines]
    
    if not grid or not grid[0]:
        print("Input grid is empty.")
        return

    # 2. Find the starting position 'S'
    start_j = -1
    start_r = -1
    
    # Assuming 'S' is in the first row (r=0), as per typical grid start
    try:
        start_j = grid[0].index('S')
        start_r = 0
    except ValueError:
        print("Starting position 'S' not found in the first row.")
        return

    # 3. Initialize state for the recursive call
    # The original code started at r=1, so we must adjust the starting point
    # to simulate the first move from 'S' at (0, start_j) to (1, start_j).
    # Since the original code did NOT check lines[i][j] for 'S', the path
    # effectively starts at (1, start_j).
    start_r_sim = 1 
    
    memo: Dict[Tuple[int, int], int] = {}
    splitter_indices: SplitterIndices = set()

    # The actual calculation starts by calling beam_down from the second row
    new_timelines = beam_down(start_r_sim, start_j, grid, memo, splitter_indices)

    print(f"Part 1 answer: {len(splitter_indices)}")
    print(f"Part 2 answer: {new_timelines}")

# --- Main Execution ---

if __name__ == "__main__":
    both()