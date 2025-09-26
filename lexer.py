import ply.lex as lex

reserved = {
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE'
}

tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'SEMICOLON',
    'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL', 'NOTEQUAL', 'EQUAL',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_GREATER = r'>'
t_LESS = r'<'
t_GREATEREQUAL = r'>='
t_LESSEQUAL = r'<='
t_NOTEQUAL = r'!='
#t_EQUAL = r'=='
#t_IF = r'if'
t_ELSE = r'else'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()

def tokenize(code):
    lexer.input(code)
    return [(tok.type, tok.value) for tok in lexer]
