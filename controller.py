import ply.lex as lex
import ply.yacc as yacc

from model import CoinSweeper

# utilities

# global command stack
commandStack = []

# wrap command in JSON response format
def makeSingleCommand(command):
    return {
            "python": command,
            "stateChanges": [
                bot.getDetails()
            ]
        }

bot = CoinSweeper.getInstance()

tokens = [
    'NUMBER',
    'MYX',
    'MYY',
    'MOVE',
    'TURNLEFT'
]

t_ignore = ' \t'


def t_MOVE(t):
    r'move'
    t.value = 'MOVE'
    return t


def t_TURNLEFT(t):
    r'turn[ ]*left'
    t.value = 'TURNLEFT'
    return t


def t_MYX(t):
    r'my[ ]*x'
    t.value = bot.myX()
    return t


def t_MYY(t):
    r'my[ ]*y'
    t.value = bot.myY()
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Invalid Token: ", t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

def p_commands(p):
    '''
    expr : expr expr
    '''

def p_command(p):
    '''
    expr : MYX
        | MYY
        | TURNLEFT
        | MOVE NUMBER
    '''
    if len(p) == 2 and p[1] == 'TURNLEFT':
        bot.turnLeft()
        commandStack.append(makeSingleCommand("turnLeft()")) 
    elif len(p) == 2 and p[1] == 'MYX':
        commandStack.append(makeSingleCommand("getX()")) 
    elif len(p) == 2:
        commandStack.append(makeSingleCommand("getY()")) 
    elif len(p) == 3:
        bot.move(p[2])
        commandStack.append(makeSingleCommand("move(" + str(p[2]) + ")")) 


def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()


def do(commands):
    commandStack.clear()
    parser.parse(commands)
    return commandStack
