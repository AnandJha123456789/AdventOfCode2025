import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

def get_lines_from_file():
    '''Reads lines from the specified file, stripping whitespace and empty lines.'''
    try:
        with open(FILE_PATH, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except IOError as e:
        print(f"Error reading file: {e}")
        return None

def solve():
    lines = get_lines_from_file()
    if lines is None:
        return

    coords = []
    for line in lines:
        coords.append(tuple(map(int, line.split(','))))

    n = len(coords)
    
    # 1. Generate all unique pairs and their distances
    # We store (distance, index_a, index_b)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            c1, c2 = coords[i], coords[j]
            dist = ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)
            edges.append((dist, i, j))

    # 2. Sort by distance (shortest first)
    edges.sort()

    # 3. Union-Find setup
    parent = list(range(n))
    size = [1] * n
    num_components = n

    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i]) # Path compression
        return parent[i]

    def union(i, j):
        nonlocal num_components
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            # Union by size
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            num_components -= 1
            return True # A merge occurred
        return False # Already connected

    # 4. Process edges
    part1_ans = None
    part2_ans = None

    for idx, (dist, i, j) in enumerate(edges):
        # We perform the union operation
        # Note: redundant connections (already in same circuit) 
        # still count towards the '1000' limit in Part 1.
        merge_happened = union(i, j)

        # PART 1: Milestone at the 1000th connection (index 999)
        if idx == 999:
            # Calculate 3 largest circuit sizes
            # Roots are elements where parent[i] == i
            all_sizes = sorted([size[k] for k in range(n) if parent[k] == k], reverse=True)
            part1_ans = all_sizes[0] * all_sizes[1] * all_sizes[2]

        # PART 2: Milestone when the very last merge happens
        if merge_happened and num_components == 1:
            part2_ans = coords[i][0] * coords[j][0]
            break

    print(f"Part 1 Answer: {part1_ans}")
    print(f"Part 2 Answer: {part2_ans}")

if __name__ == "__main__":
    solve()
