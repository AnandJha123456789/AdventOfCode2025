import os
import math
import itertools
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction

# Configuration
INPUT_FILE_NAME = 'input.txt'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, INPUT_FILE_NAME)

def get_machine_data():
    """Parses the input file into Part 1 and Part 2 data structures."""
    machines_p1 = []
    machines_p2 = []
    
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return [], []

    with open(FILE_PATH, 'r') as f:
        lines = f.read().strip().split("\n")

    for row in lines:
        if not row.strip():
            continue
        
        parts = row.split()
        
        # --- Part 1 Parsing ---
        # State: Convert [.##.] to a bitmask where # is 1
        state_str = parts[0].strip("[]")
        initial_state = 0
        for i, char in enumerate(state_str):
            if char == '#':
                initial_state |= (1 << i)
        
        # Buttons: Convert (0,2) to bitmasks
        buttons_raw = [
            list(map(int, b.strip("()").split(","))) 
            for b in parts[1:-1]
        ]
        button_masks = []
        for btn in buttons_raw:
            mask = 0
            for pos in btn:
                mask |= (1 << pos)
            button_masks.append(mask)
            
        machines_p1.append((initial_state, button_masks))

        # --- Part 2 Parsing ---
        # Joltage: {3,5,4,7} -> tuple of integers
        joltage_target = tuple(map(int, parts[-1].strip("{}").split(",")))
        
        # Buttons: Convert to counter increments (vectors)
        # (0, 3) -> Button increases counter 0 by 1 and counter 3 by 1
        button_vectors = []
        for btn in buttons_raw:
            # Determine size of this button's effect vector
            vec_len = max(btn) + 1 if btn else 0
            vec = [0] * vec_len
            for pos in btn:
                vec[pos] += 1
            button_vectors.append(tuple(vec))
            
        machines_p2.append((joltage_target, button_vectors))

    return machines_p1, machines_p2

# -----------------------------------------------------------------------------
# Part 1: Breadth-First Search (XOR State Space)
# -----------------------------------------------------------------------------

def solve_part1(machine):
    target_state, buttons = machine
    # We start at state 0 (all lights off) and want to reach target_state.
    # Operations are XOR toggles.
    
    queue = deque([(0, 0)])  # (current_state, steps)
    visited = {0}
    
    # Optimization: If target is 0, 0 steps.
    if target_state == 0:
        return 0

    while queue:
        state, steps = queue.popleft()
        
        if state == target_state:
            return steps
            
        for btn_mask in buttons:
            next_state = state ^ btn_mask
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, steps + 1))
                
    return 0

# -----------------------------------------------------------------------------
# Part 2: Linear Diophantine Equation Minimization
# -----------------------------------------------------------------------------

def reduce_matrix(mat):
    """
    Performs Gaussian elimination to put the matrix in Row Echelon Form.
    Note: This specific implementation zeroes out rows BELOW the pivot,
    leaving the upper triangle for back-substitution later.
    """
    rows = len(mat)
    if rows == 0: return
    cols = len(mat[0])
    
    cur_row = 0
    col = -1
    
    while cur_row < rows:
        col += 1
        if col >= cols:
            break

        # Find a row with a non-zero value in the current column
        pivot_row = -1
        for r in range(cur_row, rows):
            if mat[r][col] != 0:
                pivot_row = r
                break
        
        if pivot_row == -1:
            continue # Column is all zeros, move to next column

        # Swap pivot row to current position
        if pivot_row != cur_row:
            mat[cur_row], mat[pivot_row] = mat[pivot_row], mat[cur_row]

        # Normalize the pivot row so the leading coefficient is 1
        pivot_val = mat[cur_row][col]
        if pivot_val != 1:
            ratio = Fraction(1, pivot_val)
            for c in range(col, cols):
                mat[cur_row][c] *= ratio

        # Eliminate entries in rows BELOW the pivot
        for r in range(cur_row + 1, rows):
            if mat[r][col] != 0:
                factor = mat[r][col]
                # mat[r] = mat[r] - factor * mat[cur_row]
                # Doing manually to ensure Fraction precision
                pivot_row_ref = mat[cur_row] # optimization
                current_row_ref = mat[r]
                val_at_col = current_row_ref[col]
                scale = Fraction(val_at_col, pivot_row_ref[col])
                
                for c in range(cols - 1, col - 1, -1):
                    current_row_ref[c] -= pivot_row_ref[c] * scale

        cur_row += 1

def reduce_limits(basis_vectors, free_vars):
    """
    Calculates bounds [min, max] for free variables to ensure all
    dependent variables remain non-negative.
    """
    limit_updated = True
    # Initial limits: None -> [0, inf], Fixed -> [val, val]
    limits = [
        [0, math.inf] if p is None else [p, p]
        for p in free_vars
    ]

    while limit_updated:
        limit_updated = False

        for row_vec in basis_vectors:
            # row_vec represents: x_i = constant + sum(coeff_j * free_var_j)
            # We strictly require x_i >= 0
            
            for i, param_val in enumerate(free_vars):
                # We are looking to bound free_var[i]
                if param_val is not None or row_vec[i] == 0:
                    continue

                # Calculate the partial sum of the equation excluding term i
                # We want: coeff_i * p_i + partial_sum >= 0
                # partial_sum range calculation:
                constant = row_vec[-1]
                partial_sum_bounds = [-constant, -constant]
                
                for j, other_param in enumerate(free_vars):
                    if j == i or row_vec[j] == 0:
                        continue

                    coeff = row_vec[j]
                    if other_param is not None:
                        # Fixed value contribution
                        term = coeff * row_vec[j] # Wait, logic check: coeff IS row_vec[j]
                        # Original: gtsum = [g - q * val[j] ...]
                        val = other_param * coeff
                        partial_sum_bounds = [b - val for b in partial_sum_bounds]
                    else:
                        # Interval arithmetic for other free variables
                        term_bounds = sorted([coeff * limits[j][k] for k in range(2)])
                        partial_sum_bounds = [b - t for b, t in zip(partial_sum_bounds, term_bounds)]

                # Solve inequality for p_i
                # If coeff > 0: p_i >= partial_min / coeff
                # If coeff < 0: p_i <= partial_max / coeff
                coeff_i = row_vec[i]
                bounds_scaled = sorted([b / coeff_i for b in partial_sum_bounds])
                
                if coeff_i > 0:
                    if limits[i][0] < bounds_scaled[0]:
                        limits[i][0] = math.ceil(bounds_scaled[0])
                        limit_updated = True
                else:
                    if limits[i][1] > bounds_scaled[1]:
                        limits[i][1] = math.floor(bounds_scaled[1])
                        limit_updated = True

        # Check for impossibility
        if any(l[0] > l[1] if l[1] is not math.inf else False for l in limits):
            break

    return limits

def recursive_solver(basis_vectors, cost_gradient, free_vars=None):
    """
    Recursively sets free variables to find the minimum total button presses.
    basis_vectors: Matrix relating variables to free params.
    cost_gradient: Change in total presses per unit of free param.
    """
    dims = len(basis_vectors[0])
    if free_vars is None:
        free_vars = [None] * (dims - 1)
    else:
        free_vars = list(free_vars)

    # Base Case: All parameters are set
    if all(p is not None for p in free_vars):
        total = 0
        for row in basis_vectors:
            # Calculate value of this specific button count
            val = row[-1] + sum(a * b for a, b in zip(free_vars, row))
            
            # Validation: Must be non-negative integer
            if val < 0 or Fraction(val).denominator != 1:
                return math.inf
            total += val
        return total

    # Recursive Step: Narrow limits and search
    limits = reduce_limits(basis_vectors, free_vars)

    # If any limit is invalid (min > max), this path is dead
    for l in limits:
        if l[1] is not None and l[0] > l[1]:
             return math.inf

    # Heuristic: Explore the variable with the tightest finite range first
    candidates = [
        (i, l) for i, l in enumerate(limits) 
        if free_vars[i] is None
    ]
    # Sort by range size (inf - x is treated as huge)
    explore_node = min(
        candidates,
        key=lambda x: (x[1][1] if x[1][1] is not math.inf else 1e9) - x[1][0]
    )
    idx, (min_lim, max_lim) = explore_node

    # Determine step size based on denominators (LCM)
    # This ensures we step through valid rational points that could be integers
    denoms = [Fraction(v).denominator for v in [min_lim, max_lim] 
              if v is not math.inf and v is not -math.inf]
    increment = Fraction(1, math.lcm(*denoms) if denoms else 1)

    min_total = math.inf

    # Search Direction Strategy
    # If increasing this parameter increases total cost (gradient >= 0),
    # start from the minimum bound and search up.
    # Otherwise, start from maximum and search down.
    if cost_gradient[idx] >= 0:
        guess = min_lim
        is_unbounded = max_lim is math.inf
        while is_unbounded or guess <= max_lim:
            free_vars[idx] = guess
            res = recursive_solver(basis_vectors, cost_gradient, free_vars)
            
            if res < min_total:
                min_total = res
            
            # Pruning: If we found a valid result and cost is increasing, stop.
            # (Note: Logic taken from original functional script)
            if min_total is not math.inf and min_total == res and cost_gradient[idx] > 0:
                # Actually, simply break if we found a value and we are moving away from optimum
                pass 
            
            guess += increment
            # Safety break for unbounded searches if we found something
            if min_total is not math.inf and is_unbounded:
                break
    else:
        if max_lim is math.inf:
            # Should not happen in well-formed minimization unless cost goes to -inf
            raise ValueError("Unbounded negative gradient")
        
        guess = max_lim
        is_unbounded = min_lim is -math.inf
        while is_unbounded or guess >= min_lim:
            free_vars[idx] = guess
            res = recursive_solver(basis_vectors, cost_gradient, free_vars)
            
            if res < min_total:
                min_total = res
            
            guess -= increment
            if min_total is not math.inf and is_unbounded:
                break

    return min_total

def solve_part2_matrix(machine):
    target_joltage, buttons = machine
    num_rows = len(target_joltage)
    num_cols = len(buttons)

    # Build Augmented Matrix: [Buttons | Target]
    # Rows = Joltage Counters, Cols = Buttons
    matrix = [[] for _ in range(num_rows)]
    for r in range(num_rows):
        for c, btn_vec in enumerate(buttons):
            val = btn_vec[r] if r < len(btn_vec) else 0
            matrix[r].append(val)
        matrix[r].append(target_joltage[r])

    # 1. Forward Elimination (Row Echelon Form)
    reduce_matrix(matrix)

    # Count non-zero rows (constraints)
    constraints = sum(any(x != 0 for x in row) for row in matrix)
    variables = num_cols

    if variables < constraints:
        # Over-constrained, unlikely to have solution
        return 0

    # 2. Back Substitution
    # We construct 'basis_vectors' which express every button count (variable)
    # in terms of the "free" parameters.
    # Dimensions: [Variables] x [Num_Free_Params + 1 (constant)]
    
    num_free_vars = variables - constraints + 1 # Why +1 in original? 
    # Actually logic in original: dims = variables - constraints + 1. 
    # If variables == constraints, dims = 1 (just constant).
    
    dims = variables - constraints + 1
    basis_vectors = [[0] * dims for _ in range(variables)]

    param_idx = 0
    row_ptr = 0
    
    # Identify Free vs Pivot variables based on REF matrix
    # If a column doesn't have a pivot, it's a free variable.
    for col in range(variables):
        # Check if matrix[row_ptr][col] is the pivot
        if row_ptr < constraints and matrix[row_ptr][col] != 0:
            row_ptr += 1
        else:
            # This is a free variable
            basis_vectors[col][param_idx] = 1
            param_idx += 1
            
    # Perform Back Substitution to fill in Pivot variable dependencies
    # Iterating backwards from the last constraint
    for k in range(constraints - 1, -1, -1):
        # Find pivot column for this row
        pivot_col = 0
        while pivot_col < variables and matrix[k][pivot_col] == 0:
            pivot_col += 1
            
        if pivot_col == variables: continue # Row of zeros

        # Start with the constant term from the augmented matrix
        basis_vectors[pivot_col][-1] = matrix[k][-1]
        
        # Subtract dependencies on subsequent variables
        for l in range(pivot_col + 1, variables):
            factor = matrix[k][l]
            for m in range(dims):
                basis_vectors[pivot_col][m] -= factor * basis_vectors[l][m]

    # 3. Calculate Cost Gradient
    # total_presses = sum(basis_vectors[var])
    # We sum the vectors to see how total presses change with each free param
    cost_gradient = [0] * dims
    for d in range(dims):
        cost_gradient[d] = sum(v[d] for v in basis_vectors)

    # 4. Solve for Integers
    result = recursive_solver(basis_vectors, cost_gradient)
    
    return result if result != math.inf else 0

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------

def solve():
    p1_data, p2_data = get_machine_data()
    if not p1_data:
        return

    # Part 1 Execution
    with ThreadPoolExecutor() as executor:
        ans_p1 = sum(executor.map(solve_part1, p1_data))

    # Part 2 Execution
    # Note: Threading can be added here, but sequential is safer for debugging/limits
    ans_p2 = sum(map(solve_part2_matrix, p2_data))

    print(f"Part 1 answer: {ans_p1}")
    print(f"Part 2 answer: {ans_p2}")

if __name__ == "__main__":
    solve()