import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys

variables = {}

# Gramatica de asignacion de variables
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

# Gramatica de una expresion
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

def p_funciones(p):
    '''
    funciones : function Space function
                | function Space funciones
                '''
    p[0] = (p[1],p[3])


# funcion para sumar los digitos de una tupla
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


# funcion de numero aleatorio
def p_Azar(p):
    '''function : Azar Space expression'''
    num = random.randint(0,p[3])
    p[0]=num

# funcion para cambiar de signo
def p_Menos(p):
    '''function :  Menos Space expression'''
    num = -p[3]
    p[0]=num

# funcion para multiplicar los digitos de una tupla
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

# funcion para calcular potencia y gramatica
def p_Potencia(p):
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

def p_Cuenta(p):
    '''function : Cuenta Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=len(Lista)

def p_Ultimo(p):
    '''function : Ultimo Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=Lista[len(Lista)-1]

def p_Elemento(p):
    '''function : Elemento Space expression Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[6])
    p[0]=Lista[p[3]-1]

def p_Primero(p):
    '''function : Pri Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=Lista[0]

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

# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    '''function :  PonColorLapiz'''

# Funcion para poner la tortuga en el centro
def p_Centro(p):
    '''function :  Centro'''

# Funcion para pausar la ejecucion
def p_Espera(p):
    '''function :  Espera Space expression'''
    time.sleep(p[3]/60)
    print("Wait de " + str(p[3]/60) + " segundos")
# Funcion que ejecuta las Ordenes
def p_Ejecuta(p):
    '''function :  Ejecuta Space LeftSquareBracket operaciones RightSquareBracket'''

# Funcion que repite ordenes cierta cantidad de veces
def p_Repite(p):
    '''function :  Repite Space expression LeftSquareBracket function RightSquareBracket'''
    for x in range(p[3]):
        p[0] = p[5]

# Ejecuta si se cumple la condicion
def p_Si(p):
    '''function :  Si Space  operaciones LeftSquareBracket operaciones RightSquareBracket'''


# Funcion que devuelve True si la dos numeros son iguales
def iguales(tupla):
    if(tupla[0] == tupla[1]):
        return "CIERTO"
    else:
        return "FALSO"

def p_iguales(p):
    '''
    function : Iguales Space operaciones
    '''
    a= iguales(p[3])
    p[0] = a

# Funcion que devuelve CIERTO si dos condiciones se cumplen
def y(tupla):
    if(tupla[0] == "CIERTO" and tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"
def p_Y(p):
    '''
    function : Y Space function function
    '''
    print(p[3])
    res= y((p[3],p[4]))
    p[0] = res
    print(p[0])

# Funcion que devuelve CIERTO si al menos una condicion se cumple
def O(tupla):
    if(tupla[0] == "CIERTO" or tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"
def p_O(p):
    '''
    function : O Space function function
    '''
    a= O((p[3],p[4]))
    p[0] = a

# Funcion que devuelve CIERTO si n > n1
def MayorQue(tupla):
    if(type(tupla[1]) == tuple):
        if (tupla[0] > tupla[1][0]):
            return "CIERTO"
        else:
            return "FALSO"
    elif(tupla[0] > tupla[1]):
        return "CIERTO"
    else:
        return "FALSO"
def p_MayorQue(p):
    '''
    function : MayorQue Space operaciones
    '''
    a= MayorQue(p[3])
    p[0] = a
# Funcion que devuelve Falso si n < n1
def MenorQue(tupla):
    if(tupla[0] < tupla[1]):
        return "CIERTO"
    else:
        return "FALSO"
def p_MenorQue(p):
    '''
    function : MenorQue Space operaciones
    '''
    a= MenorQue(p[3])
    p[0] = a

# Funcion que redondea un numero
def p_Redondea(p):
    '''
        function : Redondea Space expression
    '''
    p[0]= round(p[3])

# Funcion que calcula el coseno de un numero
def p_Cos(p):
    '''function :  Cos Space expression'''
    num = m.cos(m.radians(p[3]))
    p[0]=num

# Funcion para restar los digitos de una tupla
def restar(tupla):
    resta=0
    while (type(tupla[1]) == tuple):
        resta += tupla[0]
        tupla = tupla[1]
    return resta - tupla[0] - tupla[1]

def p_restar(p):
    '''
    function : Diferencia Space operaciones
    '''
    a= restar(p[3])
    p[0] = a

# Retorna error de sintaxis
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
