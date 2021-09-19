import ply.lex as lex
import ply.yacc as yacc
import re as re
import logging

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
    u'ಹಂತಗಳು ಮುಂದೆ ಹೋಗಿ'
    t.value = 'MOVE'
    return t

def t_TURNLEFT(t):
    u'ಎಡಕ್ಕೆ ತಿರುಗಿ'
    t.value = 'TURNLEFT'
    return t

def t_TURNRIGHT(t):
    u'ಬಲಕ್ಕೆ ತಿರುಗಿ'
    t.value = 'TURNRIGHT'
    return t

def t_PENUP(t):
    u'ಪೆನ್ ಬಿಡಿ'
    t.value = 'PENUP'
    return t

def t_PENDOWN(t):
    u'ಪೆನ್ ಒತ್ತಿ'
    t.value = 'PENDOWN'
    return t  

def t_MYROW(t):
    u'ನನ್ನ ರೋ'
    t.value = "MYROW"
    return t

def t_MYCOLUMN(t):
    u'ನನ್ನ ಕಾಲಂ'
    t.value = "MYCOLUMN"
    return t

def t_NUMBER(t):
    u'[0-9]+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_ASSIGN(t):
    u'ಎಂಬುಡು'
    t.value = 'ASSIGN'
    return t

def t_BEGIN(t):
    u'ಆರಂಭ'
    t.value = 'BEGIN'
    return t

def t_END(t):
    u'ಅಂತ್ಯ'
    t.value = 'END'
    return t

def t_IFOBSTACLEAHEAD(t):
    u'ಮುಂದೆ ತಡೆ ಇದ್ದರೆ'
    t.value = 'IFOBSTACLEAHEAD'
    return t

def t_IFOBSTACLEBEHIND(t):
    u'ಹಿಂದೆ ತಡೆ ಇದ್ದರೆ'
    t.value = 'IFOBSTACLEBEHIND'
    return t

def t_IFOBSTACLELEFT(t):
    u'ಎಡಕ್ಕೆ ತಡೆ ಇದ್ದರೆ'
    t.value = 'IFOBSTACLELEFT'
    return t

def t_IFOBSTACLERIGHT(t):
    u'ಬಲಕ್ಕೆ ತಡೆ ಇದ್ದರೆ'
    t.value = 'IFOBSTACLERIGHT'
    return t

def t_NUMBER_OF_COINS(t):
    u'ನಾಣ್ಯಗಳ ಸಂಖ್ಯೆ'
    t.value = 'NUMBER_OF_COINS'
    return t

def t_PRINT(t):
    u'ತೋರಿಸಿ'
    t.value = 'PRINT'
    return t

def t_SUBMIT(t):
    u'ಸಲ್ಲಿಸಿ'
    t.value = 'SUBMIT'
    return t

def t_IDENTIFIER(t):
    u'[a-zA-z_][a-zA-Z0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_LTE(t):
    u'ಗಿಂತ ಕಡಿಮೆ ಅಥವಾ ಸಮವೇ'
    t.value = 'LTE'
    return t

def t_GTE(t):
    u'ಗಿಂತ ಹೆಚ್ಚು ಅಥವಾ ಸಮವೇ'
    t.value = 'GTE'
    return t

def t_LT(t):
    u'ಗಿಂತ ಕಡಿಮೆ'
    t.value = 'LT'
    return t

def t_GT(t):
    u'ಗಿಂತ ಹೆಚ್ಚು'
    t.value = 'GT'
    return t

def t_EQUALS(t):
    u'ಗೆ ಸಮವೇ'
    t.value = 'EQUALS'
    return t

def t_NOTEQUALS(t):
    u'ಗೆ ಅಸಮವೇ'
    t.value = 'NOTEQUALS'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    """Error in lexing token"""
    logging.error(f'Invalid token: {t.value[0]}')
    t.lexer.skip(1)

kannada_lexer = lex.lex(reflags=re.UNICODE)

def p_commands(p):
    '''
    expr : expr expr
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
    selection_expr : IFOBSTACLEAHEAD BEGIN expr END
                    | IFOBSTACLERIGHT BEGIN expr END
                    | IFOBSTACLEBEHIND BEGIN expr END
                    | IFOBSTACLELEFT BEGIN expr END
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
    logging.error(f'Syntax error in input: {str(p)}')

kannada_parser = yacc.yacc()