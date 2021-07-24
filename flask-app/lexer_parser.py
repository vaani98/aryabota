"""Lexer and parser module for pseudo-code"""
# pylint: disable=invalid-name,unused-argument,global-statement
import ply.lex as lex
import ply.yacc as yacc
import yaml
import json

from utils import convert_pseudocode_to_python
from control_hub import *
from grid import Grid
from coin_sweeper import CoinSweeper

"""Opening config to read grid attributes"""
with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# utilities
    
class LexerError(Exception): pass

def make_command(command, value = None):
    """Wrap command in JSON response format"""
    if command == "get_row()":
        return {
                "python": command,
                "value": bot.my_row()
               }
    elif command == "get_column()":
        return {
                "python": command,
                "value": bot.my_column()
               }
    elif "get_number_of_coins()" in command:
        return {
                "python": command,
                "number of coins": value
               }
    elif '+' in command or '-' in command or '*' in command or '/' in command or '=' in command:
        return {
                "python": command
               }
    elif command == "error()":
        return {
            "error_message": value,
        }
    else:
        return {
            "python": command,
            "stateChanges": [
                bot.get_state()
            ]
        }
    return {}

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MYROW',
    'MYCOLUMN',
    'MOVE',
    'TURNLEFT',
    'COINS',
    'IDENTIFIER',
    'ASSIGN',
    'COMMA',
    'IFCOINS',
    'IFNOOBSTACLE',
    'PRINT'
]

t_ignore = ' \t'

def t_PLUS(t):
    r'\+'
    t.value = 'PLUS'
    return t

def t_MINUS(t):
    r'\-'
    t.value = 'MINUS'
    return t

def t_TIMES(t):
    r'\*'
    t.value = 'TIMES'
    return t

def t_DIVIDE(t):
    r'\/'
    t.value = 'DIVIDE'
    return t

def t_COMMA(t):
    r'\,'
    t.value = 'COMMA'
    return t

def t_MOVE(t):
    r'move'
    t.value = 'MOVE'
    return t


def t_TURNLEFT(t):
    r'turn[ ]*left'
    t.value = 'TURNLEFT'
    return t

def t_MYROW(t):
    r'my[ ]*row'
    t.value = "MYROW"
    return t


def t_MYCOLUMN(t):
    r'my[ ]*column'
    t.value = "MYCOLUMN"
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_ASSIGN(t):
    r'is'
    t.value = 'ASSIGN'
    return t

def t_IFCOINS(t):
    r'if[ ]*coins'
    t.value = 'IFCOINS'
    return t

def t_IFNOOBSTACLE(t):
    r'if[ ]*no[ ]*obstacle'
    t.value = 'IFNOOBSTACLE'
    return t

def t_COINS(t):
    r'number[ ]*of[ ]*coins'
    t.value = 'COINS'
    return t

def t_PRINT(t):
    r'print'
    t.value = 'PRINT'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-z_][a-zA-Z0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error in lexing token"""
    print("Invalid Token: ", t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

def p_commands(p):
    '''
    expr : expr expr
    '''
    p[0] = p[1] + "\n" + p[2]

def p_command(p):
    '''
    expr : TURNLEFT
        | MOVE NUMBER
        | assign_expr
        | selection_expr
        | print_expr
    '''
    if p[1] == 'TURNLEFT':
        python_code = convert_pseudocode_to_python(p[1])
        p[0] = python_code
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        python_code = convert_pseudocode_to_python(p[1], steps = p[2])
        p[0] = python_code
    return p[0]

def p_print_expr(p):
    '''
    print_expr : PRINT value_expr
    '''
    python_code = convert_pseudocode_to_python("PRINT_VALUE", expr = p[2])
    p[0] = python_code

def p_value_expr(p):
    '''
    value_expr : MYROW
               | MYCOLUMN
               | IDENTIFIER
               | NUMBER
               | COINS
               | value_expr PLUS value_expr
               | value_expr MINUS value_expr
               | value_expr TIMES value_expr
               | value_expr DIVIDE value_expr
    '''
    if (p[1] == 'MYROW' or p[1] == 'MYCOLUMN'):
        python_code = convert_pseudocode_to_python(p[1])
    elif p[1] == 'IDENTIFIER':
        python_code = convert_pseudocode_to_python("IDENTIFIER", variable = p[1])
    elif p[1] == 'COINS':
        python_code = convert_pseudocode_to_python("GET_COINS")
    elif len(p) == 4:
        var1 = p[1]
        var2 = p[3]
        python_code = convert_pseudocode_to_python(p[2], variable1 = var1, variable2 = var2)
    else:
        python_code = convert_pseudocode_to_python("NUMBER", value = p[1])
    p[0] = python_code

def p_selection_expr(p):
    '''
    selection_expr : IFCOINS COMMA expr
                   | IFNOOBSTACLE COMMA expr
    '''
    if p[1] == 'IFCOINS':
        python_code = convert_pseudocode_to_python("IFCOINS")
        p[0] = python_code + " " + p[3]
    elif p[1] == 'IFNOOBSTACLE':
        python_code = convert_pseudocode_to_python("IFNOOBSTACLE")
        p[0] = python_code + " " + p[3]

def p_assign_expr(p):
    '''
    assign_expr : IDENTIFIER ASSIGN value_expr
    '''
    python_code = convert_pseudocode_to_python("ASSIGNMENT", variable = p[1], expr = p[3])
    p[0] = python_code
    
def p_error(p):
    """Error in parsing command"""
    print("Syntax error in input! You entered " + str(p))

parser = yacc.yacc()

def understand(commands):
    """Convert pseudo-code to Python code to execute"""
    # reinitialize response file
    with open(config["app"]["results"], "w") as results_file:
        results_file.write(json.dumps([]))
    try:
        python_program = parser.parse(commands)
    except Exception as exception:
        print(exception)
        return []
    print("Python program: ", python_program)
    exception_raised = None
    try:
        exec(python_program)
    except Exception as e:
        exception_raised = e
        print("Exception raised while parsing: ", e)
    with open(config["app"]["results"]) as results_file:
        response = json.loads(results_file.read())
    if exception_raised is not None:
        response.append({
            "error_message": str(exception_raised)
        })
    response_and_python_program = {
        "python": python_program,
        "response": response
    }
    print("Response and python program:", response_and_python_program)
    return response_and_python_program