import ply.lex as lex
import ply.yacc as yacc

from CoinSweeper import CoinSweeper
from Grid import Grid

# utilities
# global command stack
commandStack = []
variables = dict()
total_var = dict()

# wrap command in JSON response format
def makeSingleCommand(command):
    if(command == "getX()"):
        return {
                "python": command,
                "state": bot.myX()
               }
    elif(command == "getY()"):
        return {
                "python": command,
                "state": bot.myY()
               }
    return {
            "python": command,
            "stateChanges": [
                bot.getDetails()
            ]
        }

def makeCommand(command, value):
    if("getNumberOfCoins(bot.myX(), bot.myY())" in command):
        return {
                "python": command,
                "number of coins": value
               }
    elif('+' in command or '-' in command or '*' in command or '/' in command or '=' in command):
        return {
                "python": command,
                "value": value
               }

bot = CoinSweeper.getInstance()
grid = Grid.getInstance()
grid.initialize_grid()

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUAL',
    'MYX',
    'MYY',
    'MOVE',
    'TURNLEFT',
    'TURNRIGHT',
    'COINS',
    'TOTALCOINS',
    'IDENTIFIER',
    'ASSIGN'
]

t_ignore = ' \t'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL = r'='

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
    t.type = 'NUMBER'
    #print(t.value)
    return t

def t_ASSIGN(t):
    r'is'
    t.value = 'ASSIGN'
    return t

def t_COINS(t):
    r'number[ ]*of[ ]*coins'
    t.value = 'COINS' 
    return t

def t_TOTALCOINS(t):
    r'total[ ]*number[ ]*of[ ]*coins'
    t.value = 'TOTALCOINS' 
    return t

def t_IDENTIFIER(t):
    r'[a-zA-z_][a-zA-Z0-9]*'
    t.type = 'IDENTIFIER'
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
        | TURNRIGHT
        | MOVE NUMBER
        | assign_expr
    '''
    if len(p) == 2 and p[1] == 'TURNLEFT':
        bot.turnLeft()
        commandStack.append(makeSingleCommand("turnLeft()")) 
    elif len(p) == 2 and p[1] == 'TURNRIGHT':
        bot.turnRight()
        commandStack.append(makeSingleCommand("turnRight()")) 
    elif len(p) == 2 and p[1] == 'MYX':
        commandStack.append(makeSingleCommand("getX()")) 
    elif len(p) == 2 and p[1] == 'MYY':
        commandStack.append(makeSingleCommand("getY()")) 
    elif len(p) == 3:
        bot.move(p[2])
        commandStack.append(makeSingleCommand("move(" + str(p[2]) + ")")) 

def p_assign_expr(p):
    '''
    assign_expr : IDENTIFIER ASSIGN COINS
                | IDENTIFIER ASSIGN TOTALCOINS
                | IDENTIFIER ASSIGN NUMBER
                | IDENTIFIER ASSIGN IDENTIFIER PLUS IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER MINUS IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER TIMES IDENTIFIER
                | IDENTIFIER ASSIGN IDENTIFIER DIVIDE IDENTIFIER
    '''
    global variables, total_var
    #print(p[1])
    if(p[3] == 'COINS'):
        var = p[1]
        value = grid.getNumberOfCoins(bot.myX(), bot.myY())
        variables[var] = value
        print("Variables = ", variables)
        commandStack.append(makeCommand(var + " = getNumberOfCoins(bot.myX(), bot.myY())", value))
    elif(p[3] == 'TOTALCOINS'):
        var = p[1]
        value = 0
        for i in variables:
            value = value + variables[i]
        total_var[var] = value
        print("Variables = ", variables)
        print("Total value = ", total_var)
        commandStack.append(makeCommand(var + " = getTotalNumberOfCoins()", value))
    elif(len(p) == 6):
        var1 = p[1]
        var2 = p[3]
        var3 = p[5]
        if(p[4] == 'PLUS'):
            variables[var1] = variables[var2] + variables[var3]
            commandStack.append(makeCommand(var1 + " = " + var2 + '+' + var3, variables[var1]))
        elif(p[4] == 'MINUS'):
            variables[var1] = variables[var2] - variables[var3]
            commandStack.append(makeCommand(var1 + " = " + var2 + '-' + var3, variables[var1]))
        elif(p[4] == 'TIMES'):
            variables[var1] = variables[var2] * variables[var3]
            commandStack.append(makeCommand(var1 + " = " + var2 + '*' + var3, variables[var1]))
        elif(p[4] == 'DIVIDE'):
            variables[var1] = variables[var2] / variables[var3]
            commandStack.append(makeCommand(var1 + " = " + var2 + '/' + var3, variables[var1]))
        print("Variables = ",variables)
    else:
        var = p[1]
        value = p[3]
        variables[var] = value
        print("Variables = ", variables)
        commandStack.append(makeCommand(var + " = " + str(value), value))


def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

def do(commands):
    commandStack.clear()
    parser.parse(commands)
    print("Command stack",commandStack)
    return commandStack