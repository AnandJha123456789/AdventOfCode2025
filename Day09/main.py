import os
import itertools
from shapely.geometry import Polygon, box

# Configuration
INPUT_FILE_NAME = 'input.txt'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

def get_points():
    """Reads the input file and returns a list of (x, y) tuples."""
    points = []
    try:
        with open(FILE_PATH, 'r') as f:
            for line in f:
                if line.strip():
                    x, y = map(int, line.split(','))
                    points.append((x, y))
        return points
    except IOError as e:
        print(f"Error reading file: {e}")
        return []

def solve():
    points = get_points()
    if not points:
        return

    max_area_p1 = 0
    max_area_p2 = 0
    
    # Part 2 requires a Polygon object representing the red/green boundary
    # The list of points is already ordered as a loop per the puzzle description
    poly = Polygon(points)

    # Iterate through all unique pairs of red tiles
    for p1, p2 in itertools.combinations(points, 2):
        x1, y1 = p1
        x2, y2 = p2
        
        # Calculate dimensions
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        current_area = width * height

        # Part 1: Simply find the largest possible area
        if current_area > max_area_p1:
            max_area_p1 = current_area

        # Part 2: Check if the rectangle is entirely within the red/green region
        # Optimization: Only do the Shapely check if the area is potentially the new max
        if current_area > max_area_p2:
            xmin, xmax = (x1, x2) if x1 < x2 else (x2, x1)
            ymin, ymax = (y1, y2) if y1 < y2 else (y2, y1)
            
            # Create a geometric box for the candidate rectangle
            rect = box(xmin, ymin, xmax, ymax)
            
            # .covers() checks if every point of the rectangle is inside or on the boundary of the polygon
            if poly.covers(rect):
                max_area_p2 = current_area

    print(f"Part 1 answer: {max_area_p1}")
    print(f"Part 2 answer: {max_area_p2}")

if __name__ == "__main__":
    solve()