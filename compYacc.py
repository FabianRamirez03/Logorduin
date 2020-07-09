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
    '''
    p[0] = p[1]

def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = variables[p[1]]
    except LookupError:
        print("Variable no definida '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print("Error de sintaxis de '%s'" % p.value)
    else:
        print("Syntax error at EOF")


# #Gramatica que se encarga del manejo del inicializacion y creacion de variables
# def p_initializer_assignOrCreate(p):
#     """initializer : assign"""
#
# #Gramatica vacia
# def p_initializer_empty(p):
#     'initializer : '
#     print("Error, debe al menos tener una variable creada.")



# def p_expression_assign_empty(p):
#     'assign : '
#
# def p_create(p):
#     '''
#      create : NAME
#     '''
#
# def p_create_empty(p):
#     '''
#      create :
#     '''



parser = yacc.yacc()

while True:
    try:
        s = input('->')
    except EOFError:
        break
    if not s:continue
    parser.parse(s)
