import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys

variables = {}

#Gramatica de asignacion de variables
def p_statement_create(p):
    '''
    statement : Var Space NAME Space EQUALS Space expression
    '''
    if p[3] not in variables:
        p[0] = ('=', p[3], p[7])
        variables[p[3]] = p[7]
        print(variables)
    else:
        print("La variable '%s' ya fue creada" % p[3])

def p_statement_assign(p):
    """statement : Inic Space NAME Space EQUALS Space expression
                 | Inic Space NAME Space EQUALS Space function
                 """
    if p[3] not in variables:
        print("La variable '%s' no ha sido creada" % p[3])
    else:
        variables[p[3]] = p[7]


def p_statement_create_empty(p):
    '''
    statement : Var Space NAME
    '''
    p[0] = ('=', p[3], None)
    variables[p[3]] = None
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


def p_operaciones(p):
    '''
    operaciones : expression Space expression
                | expression Space operaciones
                '''
    p[0] = (p[1],p[3])

#funcion para sumar los digitos de una tupla
def suma(tupla):
    suma1=0
    while (type(tupla[1]) == tuple):
        suma1 += tupla[0]
        tupla = tupla[1]
    return suma1 + tupla[0] + tupla[1]

def p_suma(p):
    '''
    function : Suma Space operaciones
    '''
    a= suma(p[3])
    p[0] = a

def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    variables[p[3]] = variables[p[3]] + 1


def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    variables[p[3]] = variables[p[3]] + p[5]


#funcion de numero aleatorio
def p_Azar(p):
    '''function : Azar Space expression'''
    num = random.randint(0,p[3])
    p[0]=num

#funcion para cambiar de signo
def p_Menos(p):
    '''function :  Menos Space expression'''
    num = -p[3]
    p[0]=num

#funcion para multiplicar los digitos de una tupla
def producto(tupla):
    num = 1
    while (type(tupla[1]) == tuple):
        num *= tupla[0]
        tupla = tupla[1]
    return num * tupla[0] * tupla[1]

def p_producto(p):
    '''
    function : Producto Space operaciones
    '''
    p[0]=producto(p[3])

#funcion para calcular potencia y gramatica
def p_Menos(p):
    '''function :  Potencia Space expression Space expression'''
    num = p[3]**p[5]
    p[0]=num

def p_Division(p):
    '''function :  Division Space expression Space expression'''
    num = p[3]/p[5]
    p[0]=num


def p_Resto(p):
    '''function :  Resto Space expression Space expression'''
    num = p[3]%p[5]
    p[0]=num

def p_RC(p):
    '''function :  RC Space expression'''
    num = m.sqrt(p[3])
    p[0]=num

def p_Sen(p):
    '''function :  Sen Space expression'''
    num = m.sin(m.radians(p[3])) #preeeeguntaaar
    p[0]=num

def makeList(tupla):
    lista=[]
    while(type(tupla[1]) == tuple):
        lista+=[tupla[0]]
        tupla=tupla[1]
    return lista+[tupla[0]]+[tupla[1]]

def p_Elegir(p):
    '''function : Elegir Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    num= random.randint(0,len(Lista)-1)
    p[0]=Lista[num]

def p_Avanza(p):
    """
    function : Avanza Space expression
             | Avanza Space function
    """
    p[0] = p[3]
    print("Avanza '%d' unidades" %p[0])

def p_Retrocede(p):
    """
    function : Retrocede Space expression
             | Retrocede Space function
    """
    p[0] = p[3]
    print("Retrocede '%d' unidades" %p[0])

def p_GiraDerecha(p):
    """
    function : GiraDerecha Space expression
    """
    p[0] = p[3]
    print("Gira '%d' grados a la derecha" % p[0])

def p_GiraIzquierda(p):
    """
    function : GiraIzquierda Space expression
    """
    p[0] = p[3]
    print("Gira '%d' grados a la izquierda" %p[0])

def p_OcultaTortuga(p):
    """
    function : OcultaTortuga
    """
    print("Se oculta la tortuga")

def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    print("Aparece la Tortuga")

def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    a = [p[4],p[6]]
    p[0] = a

def p_PonRumbo(p):
    """
    function : PonRumbo Space expression
    """
    p[0] = p[3]
    print("Tortuga en rumbo hacia los '%d' grados" %p[0])

def p_Rumbo(p):
    """
    function : Rumbo
    """
    print("Indicar el rumbo de la tortura")

def p_PonX(p):
    """
    function : PonX Space expression
    """
    p[0] = p[3]
    print("Tortuga en la posicionX '%d'"%p[0])

def p_PonY(p):
    """
    function : PonY Space expression
    """
    p[0] = p[3]
    print("Tortuga en la posicionY '%d'" % p[0])

def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    print("Comienza a dibujar")

def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    print("Levanta el lapiz y detiene el dibujo")

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
