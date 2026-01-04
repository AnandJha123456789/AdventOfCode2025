import os
import sys
from collections import deque, defaultdict
from typing import List, Dict, Set, DefaultDict

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = 'input.txt'
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)


def parse_input(file_path: str) -> List[str]:
    """Reads lines from the file, stripping whitespace."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def parse_graph(rows: List[str]) -> Dict[str, List[str]]:
    """Parses raw strings into an adjacency list."""
    connections = {}
    for row in rows:
        source, targets = row.split(":")
        connections[source] = targets.strip().split()
    return connections


def build_inverted_graph(rows: List[str]) -> DefaultDict[str, Set[str]]:
    """
    Parses input and builds a graph where edges point from 
    children back to parents.
    """
    inverted_graph = defaultdict(set)
    for row in rows:
        parent, children_str = row.split(":")
        children = children_str.strip().split()
        for child in children:
            inverted_graph[child].add(parent)
    return inverted_graph


def topological_sort(graph: DefaultDict[str, Set[str]]) -> List[str]:
    """
    Performs an iterative topological sort using DFS.
    Returns a list of nodes in topological order.
    """
    visited = set()
    result = []

    for node in graph:
        if node in visited:
            continue

        stack = [node]
        visited.add(node)

        while stack:
            current = stack[-1]
            has_unvisited_children = False

            # Check children (which are parents in the original context)
            for neighbor in graph.get(current, []):
                if neighbor in visited:
                    continue

                has_unvisited_children = True
                visited.add(neighbor)
                stack.append(neighbor)
                break

            if not has_unvisited_children:
                result.append(stack.pop())

    result.reverse()
    return result


def count_paths_from_sources(inverted_graph: DefaultDict[str, Set[str]], target_node: str) -> Dict[str, int]:
    """
    Calculates the number of paths from every upstream node to the target_node
    using Dynamic Programming on the topologically sorted inverted graph.
    """
    path_counts = defaultdict(int)
    path_counts[target_node] = 1

    processed = set()
    sorted_nodes = topological_sort(inverted_graph)

    for node in sorted_nodes:
        current_count = path_counts[node]
        processed.add(node)

        # Propagate counts to neighbors (parents in original graph)
        for neighbor in inverted_graph.get(node, []):
            path_counts[neighbor] += current_count
            
            # Sanity check for cycles or logic errors
            if neighbor in processed:
                raise ValueError(f"Cycle detected or sort error at node {neighbor}")

    return path_counts


def part1(rows: List[str]) -> None:
    """
    Counts paths from 'you' to 'out' using a Queue-based traversal.
    """
    connections = parse_graph(rows)

    path_count = 0
    queue = deque(["you"])

    # Note: This is an exhaustive path enumeration, not a standard BFS,
    # because visited nodes are not excluded.
    while queue:
        current = queue.popleft()
        
        if current == "out":
            path_count += 1
            continue

        if current in connections:
            queue.extend(connections[current])

    print(f"Part 1 answer: {path_count}")


def part2(rows: List[str]) -> None:
    """
    Calculates paths from 'svr' to 'out' that pass through 
    both 'dac' and 'fft' using DP on the inverted graph.
    """
    inverted_graph = build_inverted_graph(rows)

    # Pre-calculate path counts from any node to these specific targets
    targets = ["out", "fft", "dac"]
    paths_to = {}
    
    for target in targets:
        paths_to[target] = count_paths_from_sources(inverted_graph, target)

    # Logic:
    # Path A: svr -> dac -> fft -> out
    # Path B: svr -> fft -> dac -> out
    
    # paths_to["dac"]["svr"] means: paths from svr TO dac
    path_a_count = (
        paths_to["dac"]["svr"] * 
        paths_to["fft"]["dac"] * 
        paths_to["out"]["fft"]
    )

    path_b_count = (
        paths_to["fft"]["svr"] * 
        paths_to["dac"]["fft"] * 
        paths_to["out"]["dac"]
    )

    total_paths = path_a_count + path_b_count
    print(f"Part 2 answer: {total_paths}")


def main():
    if not os.path.exists(FILE_PATH):
        print(f"Input file not found at: {FILE_PATH}")
        return

    rows = parse_input(FILE_PATH)
    
    part1(rows)
    part2(rows)


if __name__ == "__main__":
    main()