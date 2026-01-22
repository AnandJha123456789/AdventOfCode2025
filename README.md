# Advent of Code 2025 Solutions 🎄

This repository contains my Python solutions for **Advent of Code 2025**.

## Project Structure

The project is structured with a separate directory for each day. Each directory contains the solution code (`main.py`) and the puzzle input (`input.txt`).

```text
.
├── Day01/
│   ├── input.txt
│   └── main.py
├── Day02/
│   ├── input.txt
│   └── main.py
...
└── Day12/
    ├── input.txt
    └── main.py
```

## Getting Started

### Prerequisites

All solutions are written in **Python 3**.

Most solutions utilize the standard library, but **Day 09** requires `Shapely` for geometric calculations. You can install the necessary dependencies using pip:

```bash
python -m pip install shapely
```

### Running the Solutions

To run a specific day's solution, navigate to the directory or run the script from the root using the relative path:

```bash
# Example: Run Day 1
python Day01/main.py

# Example: Run Day 9
python Day09/main.py
```

*Note: Ensure your `input.txt` files are present in the respective Day folders before running.*

## Daily Solutions & Concepts

Here is a summary of the topics and algorithms used for the first 12 days:

| Day | Topic / Theme | Key Concepts & Algorithms |
| :--- | :--- | :--- |
| **01** | Circular Movement | Modular arithmetic, boundary tracking. |
| **02** | Pattern Matching | Integer string manipulation, palindromes, repeating block detection. |
| **03** | String Parsing | Sliding windows, digit maximization logic. |
| **04** | Cellular Automata | 2D Grid simulation, neighbor counting, state stabilization. |
| **05** | Ranges | Interval merging, range intersection, contiguous block logic. |
| **06** | Grid Math | Matrix transposition, columnar string parsing, operations (`+`, `*`). |
| **07** | Pathfinding | Recursion, Memoization, DFS with beam splitting. |
| **08** | Connectivity | **Union-Find (Disjoint Set)**, Kruskal's Algorithm, Minimum Spanning Tree logic. |
| **09** | Geometry | **Shapely** library, Polygon boundaries, Rectangle maximization. |
| **10** | State Machines | **BFS** (Part 1), **Gaussian Elimination** & Linear Diophantine Equations (Part 2). |
| **11** | Graph Theory | **Topological Sort**, Inverted graphs, Dynamic Programming (path counting). |
| **12** | Shape Fitting | 2D Shape parsing, Area heuristics, `NamedTuple` data structures. |

## Highlights

*   **Day 08** implements a custom Union-Find data structure to track component sizes and connectivity.
*   **Day 10** includes a robust linear algebra solver (row reduction) to handle complex Part 2 constraints without brute force.
*   **Day 11** performs path counting on Directed Acyclic Graphs (DAGs) using Topological Sort.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---