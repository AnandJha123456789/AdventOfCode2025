import os
from typing import Optional, List, Tuple

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

# --- Utility Functions ---

def get_ranges_from_file(file_path: str) -> Optional[List[Tuple[int, int]]]:
    """
    Reads ranges from the file. The expected format is a single line
    like 'low1-high1,low2-high2,...'
    Returns a list of tuples: [(low1, high1), (low2, high2), ...].
    """
    try:
        with open(file_path, 'r') as f:
            # Read all lines, strip, filter empty ones
            lines = [line.strip() for line in f if line.strip()]

            if not lines:
                return []

            # The input is expected to be a single line of comma-separated ranges
            range_strings = lines[0].split(',')

            ranges = []
            for r_str in range_strings:
                try:
                    # Each range is 'low-high'
                    low_str, high_str = r_str.split('-')
                    ranges.append((int(low_str), int(high_str)))
                except ValueError:
                    print(f"Skipping malformed range: {r_str}")
                    continue

        return ranges
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

# --- Part 1 Logic ---

def is_self_reflecting(number: int) -> bool:
    """Checks if a number, when treated as a string, is 'self-reflecting' (AABB, CCDD, etc.)"""
    s_num = str(number)
    length = len(s_num)

    # Must have an even length to be perfectly split into two equal halves
    if length % 2 != 0:
        return False

    midpoint = length // 2
    left_half = s_num[:midpoint]
    right_half = s_num[midpoint:]

    return left_half == right_half

def part1():
    """Calculates the sum of all numbers within the input ranges that are 'self-reflecting' (e.g., 1212, 55)."""
    ranges = get_ranges_from_file(FILE_PATH)
    if ranges is None:
        return

    valid_numbers_sum = 0
    for lower_bound, upper_bound in ranges:
        for num in range(lower_bound, upper_bound + 1):
            if is_self_reflecting(num):
                valid_numbers_sum += num
                
    print(f"Part 1 answer: {valid_numbers_sum}")

# --- Part 2 Logic ---

def is_fully_repeating_block(number: int) -> bool:
    """
    Checks if a number is composed of a single, repeating block of digits (e.g., 121212, 3333).
    This includes the Part 1 case (e.g., 1212).
    """
    s_num = str(number)
    length = len(s_num)

    # Check potential block lengths from 1 up to half the total length
    for block_len in range(1, length // 2 + 1):
        # The block length must divide the total length evenly
        if length % block_len != 0:
            continue

        # Extract the initial block
        initial_block = s_num[:block_len]
        
        # Check if the entire number is composed of this repeating block
        is_repeating = True
        for i in range(block_len, length, block_len):
            current_block = s_num[i:i + block_len]
            if current_block != initial_block:
                is_repeating = False
                break

        if is_repeating:
            # Found a repeating block pattern, so the number is valid
            return True

    return False

def part2():
    """Calculates the sum of all numbers within the input ranges that are composed of a single, repeating block of digits."""
    ranges = get_ranges_from_file(FILE_PATH)
    if ranges is None:
        return

    valid_numbers_sum = 0
    for lower_bound, upper_bound in ranges:
        for num in range(lower_bound, upper_bound + 1):
            if is_fully_repeating_block(num):
                valid_numbers_sum += num

    print(f"Part 2 answer: {valid_numbers_sum}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()