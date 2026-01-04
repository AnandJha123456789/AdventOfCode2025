import os
from typing import Optional, List

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

# --- Part 1 Logic ---

def process_line_part1(line: str) -> int:
    """
    Finds a two-digit number: the first digit is the max of all but the last digit,
    and the second digit is the max of the remaining digits after the first max's index.
    """
    # Convert string line to a list of integers
    digits = [int(v) for v in list(line)]
    
    # 1. Find the largest digit in the line, excluding the last digit
    # Note: max(digits[0:-1]) correctly handles the list up to the second-to-last element.
    try:
        left_digit = max(digits[0:-1])
    except ValueError:
        # Handles case where the list is too short (e.g., only one digit)
        return 0

    # 2. Find the index of the first occurrence of this max digit
    # The search for the index must be over the entire list up to -1, which is implicit in the logic.
    # We need the index *in the original list* to find the "remaining digits".
    # Since max() finds the largest, we assume the solution cares about the *first* occurrence
    # if there are multiple.
    left_digit_idx = -1
    for i, digit in enumerate(digits[:-1]):
        if digit == left_digit:
            left_digit_idx = i
            break
    
    if left_digit_idx == -1:
        # Should not happen if digits[:-1] is not empty
        return 0

    # 3. Find the largest digit in the remaining part of the list (from the *next* index)
    # The remaining digits start from the index *after* the left_digit was found.
    # The original logic used val.index(left_digit) + 1, which finds the index of the
    # *first* occurrence of `left_digit` in the *entire* list.
    
    # If using the index from the first occurrence in `digits[:-1]`:
    right_part = digits[left_digit_idx + 1:]
    
    try:
        right_digit = max(right_part)
    except ValueError:
        # Handles case where the right part is empty (e.g., left_digit was the second-to-last digit)
        right_digit = 0 # Defaulting to 0 if no digits remain for the second slot

    # 4. Combine into a two-digit number (Tens and Units)
    digit = left_digit * 10 + right_digit
    return digit


def part1():
    """Calculates the sum of constructed two-digit numbers based on maximization rules."""
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    output_sum = 0
    for line in lines:
        output_sum += process_line_part1(line)

    print(f"Part 1 answer: {output_sum}")

# --- Part 2 Logic ---

def process_line_part2(line: str, target_length: int = 12) -> int:
    """
    Constructs a number of target_length by iteratively picking the largest digit
    from a constrained, shrinking window of the remaining digits.
    """
    digits = [int(v) for v in list(line)]
    start_idx = 0
    constructed_value_str = ''
    
    # Pre-calculate the total number of digits available in the line
    total_len = len(digits)

    while len(constructed_value_str) < target_length:
        # Calculate the maximum *ending* index for the search window.
        # This index ensures there are exactly enough remaining digits (including the current pick)
        # to complete the final number of length `target_length`.
        # Remaining digits needed: target_length - len(constructed_value_str)
        # Max index is: total_len - (Remaining digits needed)
        
        remaining_needed = target_length - len(constructed_value_str)
        max_idx = total_len - remaining_needed
        
        # The window is digits[start_idx : max_idx + 1] (inclusive up to max_idx)
        window = digits[start_idx : max_idx + 1]
        
        if not window:
            # Should not happen if target_length is realistic, but for safety
            break 
            
        max_value = max(window)
        constructed_value_str += str(max_value)

        # Find the index of the first occurrence of max_value in the *original* list (relative to start_idx)
        # and set the new starting position (start_idx) to *after* this found index.
        for i in range(start_idx, max_idx + 1):
            if digits[i] == max_value:
                start_idx = i + 1
                break
                
    return int(constructed_value_str) if constructed_value_str else 0

def part2():
    """Calculates the sum of the numbers constructed by the iterative maximal digit selection."""
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    # Assuming the target length is constant, based on the original code's variable:
    LEN_PER_NUM = 12 
    
    output_sum = 0
    for line in lines:
        output_sum += process_line_part2(line, target_length=LEN_PER_NUM)

    print(f"Part 2 answer: {output_sum}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()