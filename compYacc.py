import ply.yacc as yacc
from compLexx import tokens
import sys


#Gramatica de asignacion de variables
def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])



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
# p_error is another special Ply function.
def p_error(p):
    print("Syntax error found!")
#Asignacion de un valor "vacio"
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

parser = yacc.yacc()
while True:
    try:
        s = input('-> ')
    except EOFError:
        break
    parser.parse(s)
