import ply.yacc as yacc
import ply.lex as lex

reserved = {}

# Define the tokens
tokens = [
    'ID',
    'NUMBER',
    'ASSIGN',
    'TRUE',
    'FALSE',
    'FLOAT',
    'NEGATIVE',
    'SEMI',
]

# Token definitions
t_NUMBER = r'\d+'
t_NEGATIVE = r'-\d+'
t_ASSIGN = r'='
t_FLOAT = r'[+-]?[0-9]*\.[0-9]+([eE][+-]?[0-9]+)?'

def t_TRUE(t):
    r'true'
    t.type = 'TRUE'
    return t

def t_FALSE(t):
    r'false'
    t.type = 'FALSE'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = ' \n\t'

# Error handling
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

def t_SEMI(t):
    r';'
    return t

# Parsing rules for variable declarations
def p_statement_declare(p):
    '''statement : ID ASSIGN NUMBER
                 | ID ASSIGN NEGATIVE
                 | ID ASSIGN FALSE
                 | ID ASSIGN FLOAT
                 | ID ASSIGN TRUE'''
    p[0] = f'{p[1]} = {p[3]}\n'

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

while True:
    try:
        s = input('Enter a Lua variable declaration: ')
    except EOFError:
        break
    if not s:
        continue
    lexer.input(s)
    for token in lexer:
        print(token)
    result = parser.parse(s, lexer=lexer)
    if result:
        print("Valid input")
        print("Generated code:")
        print(result)
    else:
        print("Invalid input. Please enter a valid Lua variable declaration.")
