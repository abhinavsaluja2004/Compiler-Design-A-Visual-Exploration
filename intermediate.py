# intermediate.py

temp_counter = 0
label_counter = 0

def new_temp():
    """Generates a new temporary variable name (e.g., t0, t1)."""
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def new_label():
    """Generates a new label name (e.g., L0, L1)."""
    global label_counter
    label = f"L{label_counter}"
    label_counter += 1
    return label

def generate_code(ast_list):
    """Main function to generate intermediate code from an AST list."""
    # Reset counters for each run
    global temp_counter, label_counter
    temp_counter = 0
    label_counter = 0
    
    final_code = []
    for node in ast_list:
        final_code.extend(walk(node))
    return final_code

def walk(node):
    """Recursively walks the AST to generate code for each node."""
    node_type = node[0]

    if node_type == 'assign':
        # Handles assignment like 'x = expression;'
        var_name = node[1]
        expr_code, expr_result = walk_expr(node[2])
        assignment_code = expr_code + [f"{var_name} = {expr_result}"]
        return assignment_code

    elif node_type == 'ifelse':
        # Handles 'if (condition) { true_block } else { false_block }'
        cond_code, cond_result = walk_expr(node[1])
        
        true_block_code = []
        for stmt in walk(node[2]):
            true_block_code.extend(stmt)
            
        false_block_code = []
        if len(node) == 4: # Checks if an else block exists
             for stmt in walk(node[3]):
                false_block_code.extend(stmt)

        false_label = new_label()
        end_label = new_label()

        if_code = cond_code
        if_code.append(f"if_false {cond_result} goto {false_label}")
        if_code.extend(true_block_code)
        if_code.append(f"goto {end_label}")
        if_code.append(f"{false_label}:")
        if_code.extend(false_block_code)
        if_code.append(f"{end_label}:")
        return if_code

    elif node_type == 'declare':
        # Handles 'int x;'
        return [f"int {node[1]};"]
    
    elif node_type == 'block':
        # Handles a block of statements { ... }
        block_code = []
        for stmt in node[1]:
            block_code.append(walk(stmt))
        return block_code
        
    # If the node is not a known statement type, it's an expression
    return walk_expr(node)[0]

def walk_expr(node):
    """
    Handles expressions. Returns a tuple of (code_list, result_variable).
    'result_variable' is the temporary variable or literal holding the expression's result.
    """
    if not isinstance(node, tuple):
        # Base case for a direct identifier or number
        return [], str(node)

    node_type = node[0]

    if node_type in ('+', '-', '*', '/', '>', '<', '>=', '<=', '!=', '=='):
        # Handles binary operations
        left_code, left_result = walk_expr(node[1])
        right_code, right_result = walk_expr(node[2])
        
        temp = new_temp()
        op_code = left_code + right_code
        op_code.append(f"{temp} = {left_result} {node_type} {right_result}")
        return op_code, temp

    elif node_type == 'num':
        # Handles a number literal
        return [], str(node[1])

    elif node_type == 'id':
        # Handles a variable identifier
        return [], node[1]
    
    return [], ""