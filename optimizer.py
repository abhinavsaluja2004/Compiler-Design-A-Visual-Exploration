# optimizer.py

def optimize(inter_code):
    """
    Performs multiple optimization passes:
    1. Constant Folding: Solves constant expressions (e.g., 5 * 2 -> 10).
    2. Copy Propagation & Dead Code Elimination: Replaces variables that just copy others
       and removes the now-unnecessary copy statements.
    """
    
    # --- Pass 1: Constant Folding ---
    folded_code = []
    for line in inter_code:
        if isinstance(line, str) and len(line.split()) == 5:
            parts = line.split()
            # Check for assignment of a binary operation
            if parts[1] == '=' and parts[2].isdigit() and parts[4].isdigit():
                try:
                    # Perform the operation
                    result = eval(f"{parts[2]} {parts[3]} {parts[4]}")
                    folded_code.append(f"{parts[0]} = {result}")
                    # print(f"Folded: {line} -> {parts[0]} = {result}") # Debug print
                    continue # Skip appending the original line
                except:
                    pass # Ignore errors from eval like division by zero
        folded_code.append(line)

    # --- Pass 2: Copy Propagation and Dead Code Elimination ---
    
    # Find all direct copies (e.g., t1 = t0)
    copies = {}
    for line in folded_code:
        if isinstance(line, str) and len(line.split()) == 3:
            dest, op, src = line.split()
            if op == '=' and (src.startswith('t') or dest.startswith('t')):
                copies[dest] = src
    
    # Propagate (substitute) the copies
    propagated_code = []
    for line in folded_code:
        # Don't propagate into the original copy statements themselves
        is_original_copy = False
        if isinstance(line, str) and len(line.split()) == 3:
             dest, _, _ = line.split()
             if dest in copies:
                 is_original_copy = True

        if not is_original_copy:
            new_line = line
            for dest, src in copies.items():
                # Replace whole words only to avoid replacing 't1' in 't10'
                new_line = new_line.replace(f" {dest}", f" {src}").replace(f"({dest}", f"({src}")
            propagated_code.append(new_line)
        else:
            # We keep the original copy for now, but will remove it later if unused
            propagated_code.append(line)

    # Determine which copy variables are actually used
    used_vars = set()
    for line in propagated_code:
        parts = line.split()
        if len(parts) >= 3:
            # Add RHS variables for lines like "t2 = t0 + t1" or "if_false t0 goto L1"
            used_vars.update(part for part in parts[1:] if part in copies)
        
    # Final pass: Remove dead code (unused copy statements)
    optimized_code = []
    for line in propagated_code:
        if isinstance(line, str) and len(line.split()) == 3:
            dest, op, src = line.split()
            # If it's a copy statement and its destination is never used, it's dead code
            if op == '=' and dest in copies and dest not in used_vars:
                # print(f"Eliminated Dead Code: {line}") # Debug print
                continue # Skip this line
        optimized_code.append(line)
        
    return optimized_code