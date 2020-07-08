import ply.yacc as yacc
import sys
parser = yacc.yacc()

#Gramatica de asignacion de variables
def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])

#Permite recursividad de expresiones matematicas
def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    # Build our tree.
    p[0] = (p[2], p[1], p[3])

#Asignacion de numeros
def p_var_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

#Asignacion del nombre a la variable
def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

#Asignacion de un valor "vacio"
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


while True:
    try:
        s = input('-> ')
    except EOFError:
        break
    parser.parse(s)