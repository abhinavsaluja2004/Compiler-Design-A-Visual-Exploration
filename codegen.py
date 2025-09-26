# codegen.py
def generate_target(opt_code):
    target = []
    reg_counter = 1  # Start register naming from R1

    for line in opt_code:
        if isinstance(line, str):
            line = line.strip()
            if line.startswith("int"):
                continue  # Skip declarations like "int a;"
            parts = line.split()

            if len(parts) == 5 and parts[1] == '=':
                # Expression: t1 = a + b
                dest, _, op1, operator, op2 = parts
                target.append(f"MOV R{reg_counter}, {op1}")
                asm_op = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV',
                    '>': 'CMPGT',
                    '<': 'CMPLT',
                    '>=': 'CMPGE',
                    '<=': 'CMPLE',
                    '==': 'CMPEQ',
                    '!=': 'CMPNE'
                }.get(operator, '???')
                target.append(f"{asm_op} R{reg_counter}, {op2}")
                target.append(f"MOV {dest}, R{reg_counter}")

            elif len(parts) == 3 and parts[1] == '=':
                # Simple assignment: a = 5 or b = t0
                dest, _, src = parts
                target.append(f"MOV R{reg_counter}, {src}")
                target.append(f"MOV {dest}, R{reg_counter}")

        elif isinstance(line, list):
            # Handling if-else blocks: if t0 goto T5, etc.
            if line[0] == 'if':
                target.append(f"if {line[1]} goto T{line[2]}")
            elif line[0] == 'goto':
                target.append(f"goto {line[1]}")

        else:
            target.append(f"# Cannot translate: {' '.join(parts)}")

    return target
