#while loop
#WHILE_LOOP 
import ply.yacc as yacc
import ply.lex as lex

reserved={'while':'WHILE','do':'DO','end':'END','print':'PRINT',}

# Define the tokens
tokens = [
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'COMPARISION',
    'NUMBER',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'STRING']+list(reserved.values())


# Token definitions
#t_WHILE = r'\b(while)\b'
t_LPAREN = r'\('
t_RPAREN = r'\)'
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type=reserved.get(t.value,'IDENTIFIER')
    return t

t_NUMBER = r'\d+'
t_ASSIGN = r'='  # Allow assignment operation
t_PLUS = r'\+'
t_MINUS = r'\-'
t_PRINT = r'print'
t_STRING = r'\"[A-Za-z\s\$\/\\!@#%\^&\*\(\)\-_\+=\{\}|\']+\"'
t_ignore=' \n\t'

def t_COMPARISION(t):
    r'<=|>|<|>='
    return t

# Error handling
def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

# Parsing rules for while loops
def p_statement_while(p):
    'statement : WHILE condition DO statements END'
    # |WHILE condition DO statements END
    p[0] = f'while {p[2]}:\n{p[4]}'

def p_statements(p):
    '''statements : statement1
                  | statement1 statement2
                  | empty'''
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = ''

def p_condition(p):
    'condition : IDENTIFIER COMPARISION NUMBER'
    p[0] = f'if {p[1]} {p[2]} {p[3]}:'

def p_statements_fori(p):
    '''statement2 : IDENTIFIER ASSIGN IDENTIFIER PLUS NUMBER 
                  | IDENTIFIER ASSIGN IDENTIFIER MINUS NUMBER '''
    p[0] = f' {p[1]}={p[3]} {p[4]} {p[5]}:'

def p_statements_print(p):
    '''statement1 : PRINT LPAREN STRING RPAREN
                 | PRINT LPAREN IDENTIFIER RPAREN'''
    p[0] = f'print({p[3]})'

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Define an empty rule
def p_empty(p):
    'empty :'
    pass

# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

while True:
    try:
        s = input('Enter a while loop (e.g., while x > 0 do print("HI") end ): ')
    except EOFError:
        break

    if not s:
        continue
    
    lexer.input(s)
    for token in lexer:
      print(token)
    parser.parse(s)

    result = parser.parse(s, lexer=lexer)
    if result:
        print("Generated code:")
        #exec(result)
        print("valid while loop")
    else:
        print("Invalid input. Please enter a valid while loop.")