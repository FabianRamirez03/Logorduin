import ply.yacc as yacc
from compLexx import tokens
import sys

variables = {}

#sintaxis para asignacion de variables
def p_statement_assign(p):
    """
    statement : NAME EQUALS expression
    """
    p[0] = ('=', p[1], p[3])
    variables[p[1]] = p[3]
    print(variables)


#Imprimir el valor de una expresion
def p_statement_expr(p):
    """
    statement : expression
    """
    p[0] = p[1]
    print(p[1])

#asignacion de valores numericos a expresiones
def p_expression_Number(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = p[1]

#asignacion de nombres a las expresiones
def p_expression_name(p):
    """
    expression : NAME
    """
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print("Variable no definida '%s'" % p[1])
        p[0] = 0

#Errores de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis de '%s'" % p.value)
    else:
        print("Error de sintaxis")



parser = yacc.yacc()

while True:
    try:
        s = input('-> ')
    except EOFError:
        break
    if not s:continue
    parser.parse(s)
