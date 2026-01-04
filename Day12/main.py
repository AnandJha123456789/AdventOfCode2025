import sys
from pathlib import Path
from typing import List, Dict, Tuple, NamedTuple, Optional

# Configuration
DEFAULT_INPUT_FILE = "input.txt"
# The user's original logic assumes every shape occupies 9 units of area.
# This is a heuristic approximation.
ASSUMED_SHAPE_AREA = 9 

class Region(NamedTuple):
    """Represents a target region under a tree."""
    width: int
    height: int
    present_counts: List[int]

    @property
    def area(self) -> int:
        return self.width * self.height

def read_input_file(filename: str) -> List[str]:
    """Reads the input file and returns a list of stripped lines."""
    file_path = Path(filename)
    if not file_path.exists():
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    try:
        return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines()]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

def parse_input(lines: List[str]) -> Tuple[Dict[int, List[List[str]]], List[Region]]:
    """
    Parses raw lines into Shapes (dictionary) and Regions (list).
    """
    shapes: Dict[int, List[List[str]]] = {}
    regions: List[Region] = []
    
    current_shape_id: Optional[int] = None

    for line in lines:
        if not line:
            continue

        # Check if line defines a grid row (contains # or .)
        if '#' in line or '.' in line:
            if current_shape_id is not None:
                shapes[current_shape_id].append(list(line))
        
        # Check if line defines a header (Shape ID or Region dimensions)
        elif ':' in line:
            header, content = line.split(":", 1)
            content = content.strip()

            if not content: 
                # Format: "0:" (This is a Shape definition)
                current_shape_id = int(header)
                shapes[current_shape_id] = []
            else:
                # Format: "12x5: 1 0 1..." (This is a Region definition)
                # Reset shape ID so we don't accidentally append to a shape
                current_shape_id = None 
                
                w_str, h_str = header.split("x")
                counts = [int(x) for x in content.split()]
                
                regions.append(Region(
                    width=int(w_str),
                    height=int(h_str),
                    present_counts=counts
                ))

    return shapes, regions

def solve_part_one(regions: List[Region]) -> int:
    """
    Determines how many regions can theoretically fit the presents based on area.
    Logic: Checks if (Total Present Count * Assumed Area) fits within Region Area.
    """
    valid_regions_count = 0

    for region in regions:
        total_presents = sum(region.present_counts)
        required_area = total_presents * ASSUMED_SHAPE_AREA

        if required_area <= region.area:
            valid_regions_count += 1

    return valid_regions_count

def solve_part_two() -> int:
    """Placeholder for Part 2 logic."""
    return 0

def main() -> None:
    # Determine input file
    filename = DEFAULT_INPUT_FILE
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    # Process Input
    lines = read_input_file(filename)
    shapes, regions = parse_input(lines)

    # Solve Part 1
    p1_answer = solve_part_one(regions)
    print(f"Part 1: {p1_answer}")

    # Solve Part 2
    p2_answer = solve_part_two()
    print(f"Part 2: {p2_answer}")

if __name__ == "__main__":
    main()