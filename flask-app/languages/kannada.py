import ply.lex as lex
import ply.yacc as yacc
import re as re

from utils import convert_kannada_pseudocode_to_python
from control_hub import *
from grid import Grid
from coin_sweeper import CoinSweeper

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

class LexerError(Exception): pass

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
    'PENUP',
    'PENDOWN',
    'NUMBER_OF_COINS',
    'IDENTIFIER',
    'ASSIGN',
    'IFOBSTACLEAHEAD',
    'IFOBSTACLEBEHIND',
    'IFOBSTACLELEFT',
    'IFOBSTACLERIGHT',
    'PRINT',
    'SUBMIT',
    'BEGIN',
    'END',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQUALS',
    'NOTEQUALS'
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
    r'hanthagalu[ ]*munde[ ]*hogu'
    t.value = 'MOVE'
    return t

def t_TURNLEFT(t):
    u'ಎಡಕ್ಕೆ ತಿರುಗಿ'
    # r'edakke[ ]*thirugi'
    t.value = 'TURNLEFT'
    return t

def t_TURNRIGHT(t):
    r'balakke[ ]*thirugi'
    t.value = 'TURNRIGHT'
    return t

def t_PENUP(t):
    r'pen[ ]*bidu'
    t.value = 'PENUP'
    return t

def t_PENDOWN(t):
    r'pen[ ]*otthu'
    t.value = 'PENDOWN'
    return t  

def t_MYROW(t):
    r'nanna[ ]*row'
    t.value = "MYROW"
    return t


def t_MYCOLUMN(t):
    r'nanna[ ]*column'
    t.value = "MYCOLUMN"
    return t


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_ASSIGN(t):
    r'embadu'
    t.value = 'ASSIGN'
    return t

def t_BEGIN(t):
    r'aarambha'
    t.value = 'BEGIN'
    return t

def t_END(t):
    r'anthya'
    t.value = 'END'
    return t

def t_IFOBSTACLEAHEAD(t):
    r'munde[ ]*thade[ ]*iddare'
    t.value = 'IFOBSTACLEAHEAD'
    return t

def t_IFOBSTACLEBEHIND(t):
    r'hinde[ ]*thade[ ]*iddare'
    t.value = 'IFOBSTACLEBEHIND'
    return t

def t_IFOBSTACLELEFT(t):
    r'edakke[ ]*thade[ ]*iddare'
    t.value = 'IFOBSTACLELEFT'
    return t

def t_IFOBSTACLERIGHT(t):
    r'balakke[ ]*thade[ ]*iddare'
    t.value = 'IFOBSTACLERIGHT'
    return t

def t_NUMBER_OF_COINS(t):
    r'naanyagala[ ]*sankhye'
    t.value = 'NUMBER_OF_COINS'
    return t

def t_PRINT(t):
    r'thorisi'
    t.value = 'PRINT'
    return t

def t_SUBMIT(t):
    r'submit'
    t.value = 'SUBMIT'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-z_][a-zA-Z0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_LTE(t):
    r'kintha[ ]*kadime[ ]*athava[ ]*samave'
    t.value = 'LTE'
    return t

def t_GTE(t):
    r'kintha[ ]*hecchu[ ]*athava[ ]*samave'
    t.value = 'GTE'
    return t

def t_LT(t):
    r'kintha[ ]*kadime'
    t.value = 'LT'
    return t

def t_GT(t):
    r'kintha[ ]*hecchu'
    t.value = 'GT'
    return t

def t_EQUALS(t):
    u'ಗೆ ಸಮವೇ'
    r'ige[ ]*samave'
    t.value = 'EQUALS'
    return t

def t_NOTEQUALS(t):
    r'ige[ ]*asamave'
    t.value = 'NOTEQUALS'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error in lexing token"""
    print("Invalid Token: ", t.value[0])
    t.lexer.skip(1)

kannada_lexer = lex.lex(reflags=re.UNICODE)

def p_commands(p):
    '''
    exprs : expr expr
        | expr
    '''
    if(len(p)==3):
        p[0] = p[1] + "\n" + p[2]
    else:
        p[0] = p[1]

def p_command(p):
    '''
    expr : TURNLEFT
        | TURNRIGHT
        | PENUP
        | PENDOWN
        | NUMBER MOVE
        | assign_expr
        | selection_expr
        | print_expr
        | submit_expr
    '''
    if p[1] in ['TURNLEFT', 'TURNRIGHT', 'PENUP', 'PENDOWN']:
        python_code = convert_kannada_pseudocode_to_python(p[1])
        p[0] = python_code
    elif len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        python_code = convert_kannada_pseudocode_to_python(p[2], steps = p[1])
        p[0] = python_code
    return p[0]

def p_print_expr(p):
    '''
    print_expr : value_expr PRINT
    '''
    print(list(p))
    python_code = convert_kannada_pseudocode_to_python("PRINT_VALUE", expr = p[1])
    p[0] = python_code

def p_value_expr(p):
    '''
    value_expr : MYROW
               | MYCOLUMN
               | IDENTIFIER
               | NUMBER
               | NUMBER_OF_COINS
               | value_expr PLUS value_expr
               | value_expr MINUS value_expr
               | value_expr TIMES value_expr
               | value_expr DIVIDE value_expr
               | value_expr value_expr LTE
               | value_expr value_expr GTE
               | value_expr value_expr LT
               | value_expr value_expr GT
               | value_expr value_expr EQUALS
               | value_expr value_expr NOTEQUALS
    '''
    if (p[1] == 'MYROW' or p[1] == 'MYCOLUMN'):
        python_code = convert_kannada_pseudocode_to_python(p[1])
    elif p[1] == 'IDENTIFIER':
        python_code = convert_kannada_pseudocode_to_python("IDENTIFIER", variable = p[1])
    elif p[1] == 'NUMBER_OF_COINS':
        python_code = convert_kannada_pseudocode_to_python("GET_COINS")
    elif len(p) == 4:
        var1 = p[1]
        var2 = p[3]
        python_code = convert_kannada_pseudocode_to_python(p[2], variable1 = var1, variable2 = var2)
    else:
        python_code = convert_kannada_pseudocode_to_python("NUMBER", value = p[1])
    p[0] = python_code

def p_selection_expr(p):
    '''
    selection_expr : IFOBSTACLEAHEAD BEGIN exprs END
                    | IFOBSTACLERIGHT BEGIN exprs END
                    | IFOBSTACLEBEHIND BEGIN exprs END
                    | IFOBSTACLELEFT BEGIN exprs END
    '''
    p[3] = '\n\t' + p[3].replace('\n', '\n\t')
    python_code = convert_kannada_pseudocode_to_python(p[1])
    p[0] = python_code + " " + p[3]

def p_assign_expr(p):
    '''
    assign_expr : IDENTIFIER ASSIGN value_expr
    '''
    python_code = convert_kannada_pseudocode_to_python("ASSIGNMENT", variable = p[1], expr = p[3])
    p[0] = python_code

def p_submit_expr(p):
    '''
    submit_expr : SUBMIT
                | SUBMIT value_expr
    '''
    if len(p) == 3:
        python_code = convert_kannada_pseudocode_to_python("SUBMIT", value = p[2])
    elif len(p) == 2:
        python_code = convert_kannada_pseudocode_to_python("SUBMIT", value = '')
    p[0] = python_code
    
def p_error(p):
    """Error in parsing command"""
    print("Syntax error in input! You entered " + str(p))

kannada_parser = yacc.yacc()