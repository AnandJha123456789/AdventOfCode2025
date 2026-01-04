import os
from typing import Optional, List, Tuple

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

Range = Tuple[int, int]

# --- Utility Functions ---

def parse_input_file(file_path: str) -> Optional[Tuple[List[Range], List[int]]]:
    """
    Reads and parses the input file, which is expected to contain a section of
    'low-high' ranges followed by a section of single numbers. The sections are
    separated by an empty line (which is removed by get_lines_from_file, so we look
    for the change in line format).

    Returns: ([valid_ranges], [check_numbers])
    """
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f]
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

    valid_ranges: List[Range] = []
    check_numbers: List[int] = []
    
    # State tracking
    parsing_ranges = True
    
    for line in lines:
        stripped_line = line.strip()
        
        if not stripped_line:
            # Empty line separator
            parsing_ranges = False
            continue

        if parsing_ranges:
            # Parse as range 'low-high'
            try:
                low_str, high_str = stripped_line.split('-')
                valid_ranges.append((int(low_str), int(high_str)))
            except ValueError:
                # If parsing a range fails, assume the range section is over
                # and this line might be the start of the check numbers (or malformed).
                # We'll re-process this line as a check number if it's not a range.
                parsing_ranges = False
                if stripped_line.isdigit():
                    check_numbers.append(int(stripped_line))
                else:
                    print(f"Skipping malformed range/line: {stripped_line}")
        else:
            # Parse as single number
            try:
                check_numbers.append(int(stripped_line))
            except ValueError:
                print(f"Skipping non-numeric check value: {stripped_line}")

    return valid_ranges, check_numbers

# --- Part 1 Logic ---

def part1():
    """
    Calculates the number of check numbers that fall within any of the defined ranges.
    """
    parsed_data = parse_input_file(FILE_PATH)
    if parsed_data is None:
        return

    valid_ranges, check_numbers = parsed_data
    
    output_count = 0

    for num in check_numbers:
        for lower_bound, upper_bound in valid_ranges:
            if lower_bound <= num <= upper_bound:
                output_count += 1
                break # Move to the next check number once a match is found
                
    print(f"Part 1 answer: {output_count}")

# --- Part 2 Logic ---

def merge_ranges(ranges: List[Range]) -> List[Range]:
    """
    Merges overlapping and contiguous ranges in a list.
    """
    if not ranges:
        return []

    # 1. Sort the ranges by their start (lower) bound
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    
    merged_ranges: List[Range] = []
    curr_lower_bound, curr_upper_bound = sorted_ranges[0]

    for next_lower_bound, next_upper_bound in sorted_ranges[1:]:
        # If the next range overlaps or is contiguous (next_low <= curr_high + 1)
        # Note: Your original logic was just 'next_low <= curr_high', which only
        # handles overlapping, but for Advent of Code problems, contiguous ranges
        # (e.g., [1,5] and [6,10]) are usually intended to be merged.
        if next_lower_bound <= curr_upper_bound + 1:
            # Extend the current merged range
            curr_upper_bound = max(curr_upper_bound, next_upper_bound)
        else:
            # The next range is completely separate, so finalize the current one
            merged_ranges.append((curr_lower_bound, curr_upper_bound))
            # Start a new merged range
            curr_lower_bound, curr_upper_bound = next_lower_bound, next_upper_bound

    # Append the last (or only) merged range
    merged_ranges.append((curr_lower_bound, curr_upper_bound))
    
    return merged_ranges


def part2():
    """
    Calculates the total number of integers covered by all ranges after merging 
    overlapping and contiguous ranges.
    """
    parsed_data = parse_input_file(FILE_PATH)
    if parsed_data is None:
        return

    valid_ranges, _ = parsed_data
    
    merged_ranges = merge_ranges(valid_ranges)

    total_coverage = 0
    for lower_bound, upper_bound in merged_ranges:
        # Number of integers in a range [a, b] is b - a + 1
        total_coverage += upper_bound - lower_bound + 1
        
    print(f"Part 2 answer: {total_coverage}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()