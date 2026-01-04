import os
from typing import Optional, List, Tuple

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

# --- Utility Functions ---

def get_lines_from_file(file_path: str) -> Optional[List[str]]:
    """Reads non-empty, stripped lines from the specified file."""
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip('\r\n') for line in f if line.strip('\r\n')] # Use strip('\r\n') to keep internal spaces
        return lines
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

# --- Part 1 Logic (Unchanged, seems correct) ---

def part1():
    """
    Processes the input as a grid of space-separated values.
    Transposes the grid, then for each new row (original column), performs 
    addition or multiplication based on the operator in the last element of the row.
    """
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    # 1. Parse the input lines into a grid of strings
    values_grid: List[List[str]] = []
    for line in lines:
        values_grid.append(line.split())

    if not values_grid or not values_grid[0]:
        print("Input grid is empty or malformed.")
        return

    # 2. Transpose the grid
    num_cols = len(values_grid[0])
    num_rows = len(values_grid)
    transposed_grid: List[List[str]] = []
    
    for j in range(num_cols):
        column_values: List[str] = []
        for i in range(num_rows):
            if j < len(values_grid[i]):
                column_values.append(values_grid[i][j])
        transposed_grid.append(column_values)

    # 3. Calculate the output based on the last element (operator) in each transposed row
    output = 0
    for row in transposed_grid:
        if not row:
            continue
            
        operator = row[-1]
        operands = [int(val) for val in row[:-1] if val.isdigit() or (val.startswith('-') and val[1:].isdigit())]
        
        curr_output = 0
        if operator == '+':
            curr_output = sum(operands)
        elif operator == '*' or operator not in ['+']: # Assuming multiplication or default
            curr_output = 1
            for val in operands:
                curr_output *= val
        
        output += curr_output
        
    print(f"Part 1 answer: {output}")

# --- Part 2 Logic (Corrected to match original intent) ---

def part2():
    """
    Processes the input by:
    1. Combining characters from all but the last line, by column index, to form multi-digit numbers.
    2. Grouping these numbers by empty (space-only) columns.
    3. Applying the operation from the last line to each group.
    """
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    if len(lines) < 2:
        print("Input too short for Part 2.")
        return

    # Last line contains the commands
    commands = lines[-1].split()
    
    # Lines containing the numbers (all but the last)
    number_lines = lines[:-1]
    
    # Determine the maximum width of the number lines
    max_col_len = max(len(line) for line in number_lines) if number_lines else 0

    # A list of lists, where each inner list is a group of numbers for a command
    transposed_groups: List[List[int]] = []
    curr_nums_group: List[int] = []

    # 1. Iterate over columns (j) and build numbers/groups
    for j in range(max_col_len):
        char_list: List[str] = []
        is_empty_column = True
        
        # Build the vertical string for column j
        for i in range(len(number_lines)):
            if j < len(number_lines[i]):
                char = number_lines[i][j]
                char_list.append(char)
                if not char.isspace():
                    is_empty_column = False
            else:
                # If the line is shorter, treat the "missing" char as a space
                char_list.append(' ')

        num_str_combined = "".join(char_list)
        
        # Check if the column is an "empty column"
        # The original logic used `if num.split() == []`, which means the string 
        # contains only whitespace (or is empty).
        if num_str_combined.strip() == "": 
            # Found an empty column: finalize the current group
            if curr_nums_group:
                transposed_groups.append(curr_nums_group)
                curr_nums_group = []
        else:
            # Found a data column: process the number
            # Original logic used int("".join(num.split())) which removes internal spaces, 
            # e.g., "1 2" -> "12"
            num_val_str = "".join(num_str_combined.split()) 
            
            try:
                num_val = int(num_val_str)
                curr_nums_group.append(num_val)
            except ValueError:
                # print(f"Skipping non-numeric column value: {num_val_str}")
                pass # Treat as if the column was invalid/not a number

    # 2. Append the last group if it exists
    if curr_nums_group:
        transposed_groups.append(curr_nums_group)

    # 3. Calculate the output using the commands
    output = 0
    
    # Iterate over commands and corresponding groups
    for i in range(min(len(transposed_groups), len(commands))):
        group = transposed_groups[i]
        command = commands[i]
        
        curr_output = 0
        if command == '+':
            curr_output = sum(group)
        elif command == '*' or command not in ['+']: # Assuming multiplication or default
            curr_output = 1
            for val in group:
                curr_output *= val
        
        output += curr_output
    
    print(f"Part 2 answer: {output}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()