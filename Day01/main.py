import os
import math
from typing import Optional, List

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

MODULUS = 100
START_POSITION = 50

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

def part1():
    """Calculates the number of times the position lands exactly on 0."""
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    current_position = START_POSITION
    zero_hits = 0

    for line in lines:
        direction = line[0]
        try:
            distance = int(line[1:])
        except ValueError:
            print(f"Skipping invalid line: {line}")
            continue

        if direction == 'L':
            current_position = (current_position - distance) % MODULUS
        elif direction == 'R':
            current_position = (current_position + distance) % MODULUS

        if current_position == 0:
            zero_hits += 1

    print(f"Part 1 answer: {zero_hits}")

# --- Part 2 Logic ---

def part2():
    """Calculates the total number of times the position crosses the 0 point (the boundary between MODULUS-1 and 0)."""
    lines = get_lines_from_file(FILE_PATH)
    if lines is None:
        return

    current_position = START_POSITION
    total_zero_crossings = 0

    for line in lines:
        direction = line[0]
        try:
            distance = int(line[1:])
        except ValueError:
            print(f"Skipping invalid line: {line}")
            continue

        P_start = current_position
        zeros_in_rotation = 0

        if direction == 'R':
            # Number of times the position crosses 0 is the number of full MODULUS segments covered.
            # Integer division achieves floor for positive numbers.
            zeros_in_rotation = (P_start + distance) // MODULUS
        
        elif direction == 'L':
            # This logic handles how many times the rotation passes 0 moving left.
            if P_start == 0:
                # If starting at 0, a cross occurs after passing the full MODULUS boundary.
                # e.g., L100 crosses once; L99 crosses zero times.
                zeros_in_rotation = (distance - 1) // MODULUS
            else:
                if distance < P_start:
                    # Not enough distance to reach or cross 0
                    zeros_in_rotation = 0
                else:
                    # 1 for the initial pass from P_start to 0
                    D_remaining = distance - P_start
                    # Then, standard full rotations for the remaining distance
                    zeros_in_rotation = 1 + (D_remaining // MODULUS)
        
        total_zero_crossings += zeros_in_rotation

        if direction == 'R':
            current_position = (P_start + distance) % MODULUS
        elif direction == 'L':
            current_position = (P_start - distance) % MODULUS
        
    print(f"Part 2 answer: {total_zero_crossings}")

# --- Main Execution ---

if __name__ == "__main__":
    part1()
    part2()