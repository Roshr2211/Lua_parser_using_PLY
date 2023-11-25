#for loop
import ply.yacc as yacc
import ply.lex as lex

# Define reserved words
reserved = {
    'for': 'FOR',
    'print': 'PRINT',
    'do': 'DO',
    'end': 'END',
}

# Define the tokens
tokens = [
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'ASSIGN',
    'COMMA',
    'NUMBER',
    'STRING',
] + list(reserved.values())

# Token definitions

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'='
t_COMMA = r','
t_STRING = r'\"[A-Za-z\s\$\/\\!@#%\^&\*\(\)\-_\+=\{\}|\']+\"'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zAZ0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

t_NUMBER = r'\d+'

# Ignore whitespace and tabs
t_ignore = ' \t'

# Error handling
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

# Parsing rules for the "for loop" and "print" statements
def p_statement_for_loop(p):
    'statement : FOR IDENTIFIER ASSIGN NUMBER COMMA NUMBER COMMA NUMBER DO statement END'
    p[0] = f'for {p[2]} = {p[4], p[6], p[8]} do\n{p[10]}\nend'

def p_statement_print(p):
    '''statement : PRINT LPAREN STRING RPAREN
                 | PRINT LPAREN IDENTIFIER RPAREN'''
    p[0] = f'print({p[3]})'

def p_statement(p):
    'statement : FOR IDENTIFIER ASSIGN NUMBER COMMA NUMBER COMMA NUMBER DO statements END'
    p[0] = f'for {p[2]} = {p[4], p[6], p[8]} do\n{p[10]}\nend'

def p_statements(p):
    'statements : statement'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

while True:
    try:
        s = input('Enter a for statement: ')
    except EOFError:
        break

    if not s:
        continue

    lexer.input(s)
    for token in lexer:
        print(token)

    result = parser.parse(s)
    if result:
        print("valid input")
        print("Generated Lua code:")
        #print(result)
    else:
        print("Invalid input. Please enter a valid for loop")