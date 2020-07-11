import ply.yacc as yacc
import random
import math as m
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
#                | expression Space expression Space RightSquareBracket
 #   '''
    p[0] = (p[1],p[3])
    print(p[0])

#funcion para sumar los digitos de una tupla
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

#funcion de numero aleatorio
def p_Azar(p):
    '''function : Azar Space expression'''
    num = random.randint(0,p[3])
    print(num)

#funcion para cambiar de signo
def p_Menos(p):
    '''function :  Menos Space expression'''
    num = -p[3]
    print(num)

#funcion para multiplicar los digitos de una tupla
def producto(numeros, num):
    if(type(numeros[1])!=tuple):
        print(num*numeros[0]*numeros[1])
    else:
        a = numeros[1]
        b = num*numeros[0]
        producto(a,b)

def p_producto(p):
    '''function : Producto Space operaciones
                '''
    producto(p[3],1)

#funcion para calcular potencia y gramatica
def p_Menos(p):
    '''function :  Potencia Space expression Space expression'''
    num = p[3]**p[5]
    print(num)

def p_Division(p):
    '''function :  Division Space expression Space expression'''
    num = p[3]/p[5]
    print(num)


def p_Resto(p):
    '''function :  Resto Space expression Space expression'''
    num = p[3]%p[5]
    print(num)

def p_RC(p):
    '''function :  RC Space expression'''
    num = m.sqrt(p[3])
    print(num)

def p_Sen(p):
    '''function :  Sen Space expression'''
    num = m.sin(m.radians(p[3])) #preeeeguntaaar
    print(num)

def makeList(tupla,lista):
    if (type(tupla[1]) != tuple):
        lista += [tupla[0]] + [tupla[1]]
        print(lista)
        return lista
    else:
        a = tupla[1]
        b = lista + [tupla[0]]
        makeList(a, b)

def p_Elegir(p):
    '''function : Elegir Space LeftSquareBracket operaciones RightSquareBracket'''
    #Lista= makeList(p[5],[])
    print(makeList(p[4],[]))
    num= random.randint(0,len(p[5]))
    print(num)
    #print(Lista[0])

def p_Borrapantalla(p):
    '''function :  Borrapantalla'''


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
