import ply.yacc as yacc
from compLexx import tokens
import sys

variables = {}

#Gramatica de asignacion de variables
def p_statement_assign(p):
    '''
    statement : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])
    variables[p[1]] = p[3]
    print(variables)

#Gramatica de una expresion
def p_statement_expr(p):
    '''
    statement : expression
    '''
    p[0] = p[1]
    print(p[1])

def p_expression_Number(p):
    '''expression : INT
                  | FLOAT
                  | function
    '''
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print("Variable no definida '%s'" % p[1])
        p[0] = 0

def p_Suma(p):
    '''function : Suma Space expression Space expression
                '''
    print(p[3]+p[5])


def p_error(p):
    if p:
        print("Error de sintaxis de '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

while True:
    try:
        s = input('->')
    except EOFError:
        break
    if not s:continue
    parser.parse(s)
