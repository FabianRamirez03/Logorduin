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
    #print(p[1])



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


def p_operaciones(p):
    '''
    operaciones : expression Space expression
           | expression Space operaciones
    '''
    p[0] = (p[1],p[3])
    #print(p[0])
def suma(numeros, suma1):
    if(type(numeros[1])!=tuple):
        print(suma1+numeros[0]+numeros[1])
    else:
        a = numeros[1]
        b = suma1+numeros[0]
        suma(a,b)

def p_suma(p):
    '''function : Suma Space operaciones
                '''
    suma(p[3],0)


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
