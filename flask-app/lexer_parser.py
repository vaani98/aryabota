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
# global command stack
commandStack = []
variables = dict()
total_var = dict()
    
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
    'TURNRIGHT',
    'COINS',
    'IDENTIFIER',
    'ASSIGN',
    'COMMA',
    'IFCOINS',
    'ANSWER'
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

def t_TURNRIGHT(t):
    r'turn[ ]*right'
    t.value = 'TURNRIGHT'
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
    r'if[ ]*there[ ]*are[ ]*coins'
    t.value = 'IFCOINS'
    return t

def t_COINS(t):
    r'number[ ]*of[ ]*coins'
    t.value = 'COINS'
    return t

def t_ANSWER(t):
    r'answer'
    t.type = 'ANSWER'
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

def p_command(p):
    '''
    expr : MYROW
        | MYCOLUMN
        | TURNLEFT
        | TURNRIGHT
        | MOVE NUMBER
        | assign_expr
        | selection_expr
        | answer_expr
    '''
    if len(p) == 2:
        python_code = convert_pseudocode_to_python(p[1])
    elif len(p) == 3:
        python_code = convert_pseudocode_to_python(p[1], steps = p[2])
    commandStack.append(python_code)

def p_answer_expr(p):
    '''
    answer_expr : ANSWER IDENTIFIER
    '''
    var = p[2]
    value = variables[var]
    # commandStack.append(make_command(var + " = " + str(value), value))

def p_selection_expr(p):
    '''
    selection_expr : IFCOINS COMMA assign_expr
    '''
    print("Variables = ", variables)

def p_assign_expr(p):
    '''
    assign_expr : IDENTIFIER ASSIGN COINS
                | IDENTIFIER ASSIGN NUMBER
                | IDENTIFIER ASSIGN IDENTIFIER PLUS IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER MINUS IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER TIMES IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER DIVIDE IDENTIFIER
    '''
    global variables, total_var
    if p[3] == 'COINS':
        var = p[1]
        value = grid.get_number_of_coins(bot.my_row(), bot.my_column())
        variables[var] = value
        print("Variables = ", variables)
        commandStack.append(make_command(var + " = get_number_of_coins()", value))
    elif len(p) == 6:
        var1 = p[1]
        var2 = p[3]
        var3 = p[5]
        if p[4] == 'PLUS':
            variables[var1] = variables[var2] + variables[var3]
            commandStack.append(make_command(var1 + " = " + var2 + '+' + var3, variables[var1]))
        elif p[4] == 'MINUS':
            variables[var1] = variables[var2] - variables[var3]
            commandStack.append(make_command(var1 + " = " + var2 + '-' + var3, variables[var1]))
        elif p[4] == 'TIMES':
            variables[var1] = variables[var2] * variables[var3]
            commandStack.append(make_command(var1 + " = " + var2 + '*' + var3, variables[var1]))
        elif p[4] == 'DIVIDE':
            variables[var1] = variables[var2] / variables[var3]
            commandStack.append(make_command(var1 + " = " + var2 + '/' + var3, variables[var1]))
        print("Variables = ",variables)
    else:
        var = p[1]
        value = p[3]
        variables[var] = value
        print("Variables = ", variables)
        commandStack.append(make_command(var + " = " + str(value), value))


def p_error(p):
    """Error in parsing command"""
    print("Syntax error in input! You entered " + str(p))

parser = yacc.yacc()

def understand(commands):
    """Convert pseudo-code to Python code to execute"""
    # reinitialize response file
    with open(config["app"]["results"], "w") as results_file:
        results_file.write(json.dumps([]))
    commandStack.clear()
    try:
        parser.parse(commands)
    except Exception as exception:
        print(exception)
        return commandStack
    python_program = "\n".join(commandStack)
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
    print(response_and_python_program)
    return response_and_python_program

def get_initial_state():
    grid_state = grid.get_state()
    coin_sweeper_state = bot.get_state()
    grid_state.update(coin_sweeper_state)
    return grid_state
