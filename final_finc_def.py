import ply.lex as lex
import ply.yacc as yacc

# Define the lexer (tokenizer)
tokens = (
    'FUNCTION',
    'ID',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'END',
)


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','

def t_END(t):
    r'end\b'
    return t


def t_FUNCTION(t):
    r'function\b'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'ID'
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Define the parser rules for Lua function declarations
def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN param_list RPAREN END'''
    p[0] = f'def {p[2]}({p[4]}):\n    pass\n'

def p_optional_function_name(p):
    '''optional_function_name : ID
                             | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_param_list(p):
    '''param_list : ID COMMA param_list
                 | ID'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]}, {p[3]}'

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error")

parser = yacc.yacc()

while True:
    # Read user input
    input_string = input("Enter a Lua function declaration (or type 'exit' to quit): ")

    if input_string.lower() == 'exit':
        break

    # Parsing the user input
    
    if not input_string:
        continue

    lexer.input(input_string)
    for token in lexer:
        print(token)
    result = parser.parse(input_string)
    
    if result:
        print("valid function definition\n")
        print(f"Generated Python code:\n{result}")
    else:
        print("Invalid function declaration")
