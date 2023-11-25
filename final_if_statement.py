import ply.yacc as yacc
import ply.lex as lex

# Define reserved words
reserved = {
    'if': 'IF',
    'print': 'PRINT',
    'then': 'THEN',
    'end' : 'END',
}

# Define the tokens
tokens = [
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'ASSIGN',
    'NUMBER',
    'STRING',
    'LT',
    'GT',
    'PIPE',
    'MINUS',
    'PLUS',
    'MULT',
    'DIV',
    'FLOAT',
    'FALSE',
    'TRUE',
    'EQUAL',
    'AMPERSAND',
] + list(reserved.values())

# Token definitions
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'=='
t_EQUAL = r'='
t_FLOAT = r'[+-]?[0-9]*\.[0-9]+([eE][+-]?[0-9]+)?'
t_STRING = r'\"[A-Za-z\d\s\$\/\\!@#%\^&\*\(\)\-_\+=\{\}|\']+\"'
t_LT = r'<'
t_GT = r'>'
t_PIPE = r'\|'
t_AMPERSAND = r'&'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\%'
t_FALSE = r'false'
t_TRUE = r'true'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_NUMBER = r'\d+'

# Ignore whitespace and tabs
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

# Parsing rules for the "if" condition and "print" statements
def p_statement_if(p):
    'statement : IF condition THEN statements END'
    p[0] = f'if {p[2]} then\n{p[4]}\nend'

def p_condition(p):
    '''condition : IDENTIFIER ASSIGN NUMBER
                | IDENTIFIER LT NUMBER
                | IDENTIFIER GT NUMBER
                | IDENTIFIER ASSIGN STRING
                | IDENTIFIER PIPE STRING
                | IDENTIFIER AMPERSAND STRING
                | NUMBER GT NUMBER
                | NUMBER LT NUMBER 
                | NUMBER ASSIGN NUMBER
                | NUMBER PIPE NUMBER
                | NUMBER AMPERSAND NUMBER'''
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_statements(p):
    '''statements : statement
                | statements statement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_statements_fori(p):
    '''statement : IDENTIFIER EQUAL IDENTIFIER PLUS NUMBER 
                | IDENTIFIER EQUAL IDENTIFIER MINUS NUMBER
                | IDENTIFIER EQUAL IDENTIFIER MULT NUMBER
                | IDENTIFIER EQUAL IDENTIFIER DIV NUMBER '''
    p[0] = f'{p[1]}={p[3]} {p[4]} {p[5]}:'

def p_statements_assign(p):
    '''statement : IDENTIFIER EQUAL FLOAT
                | IDENTIFIER EQUAL NUMBER
                | IDENTIFIER EQUAL FALSE
                | IDENTIFIER PLUS PLUS
                | IDENTIFIER MINUS MINUS
                | IDENTIFIER EQUAL TRUE'''
    p[0] = f'{p[1]}={p[3]}:'

def p_statements_print(p):
    '''statement : PRINT LPAREN STRING RPAREN
                | PRINT LPAREN IDENTIFIER RPAREN'''
    p[0] = f'print({p[3]})'

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

while True:
    try:
        s = input('Enter an "if" condition ')
    except EOFError:
        break

    if not s:
        continue

    lexer.input(s)
    for token in lexer:
        print(token)

    result = parser.parse(s)
    if result:
        print("Valid input")
        print("Generated Lua code")
        print(result)
    else:
        print("Invalid input. Please enter a valid 'if' condition.")
