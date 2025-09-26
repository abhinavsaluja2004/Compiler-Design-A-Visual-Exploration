def semantic_check(ast_list):
    errors = []
    declared_vars = set()

    for stmt in ast_list:
        if stmt[0] == 'declare':
            var_name = stmt[1]
            if var_name in declared_vars:
                errors.append(f"Semantic Error: Variable '{var_name}' already declared.")
            else:
                declared_vars.add(var_name)
        elif stmt[0] == 'assign':
            var_name = stmt[1]
            if var_name not in declared_vars:
                errors.append(f"Semantic Error: Variable '{var_name}' used before declaration.")
            check_expr(stmt[2], declared_vars, errors)

        elif stmt[0] == 'ifelse':
            # Check if the variables used in the conditional expression are declared
            check_expr(stmt[1], declared_vars, errors)
            check_expr(stmt[2], declared_vars, errors)
            check_expr(stmt[3], declared_vars, errors)

    return errors


def check_expr(expr, declared_vars, errors):
    if isinstance(expr, tuple):
        if expr[0] == 'id':
            if expr[1] not in declared_vars:
                errors.append(f"Semantic Error: Variable '{expr[1]}' used before declaration.")
        elif expr[0] in ('+', '-', '*', '/'):
            check_expr(expr[1], declared_vars, errors)
            check_expr(expr[2], declared_vars, errors)
