import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys
global Entrada
variables = {}

# Gramatica de asignacion de variables
def p_statement_create(p):
    '''
    statement : Var Space NAME Space EQUALS Space expression
    '''
    if p[3] not in variables:
        p[0] =(p[1], p[7][1], p[3] )
        variables[p[3]] = p[7][1]
        print(p[0])
        print(variables)
    else:
        print("La variable '%s' ya fue creada" % p[3])

def p_statement_assign(p):
    """
    function : Inic Space NAME Space EQUALS Space expression
             | Inic Space NAME Space EQUALS Space function
    """
    if p[3] not in variables:
        print("La variable '%s' no ha sido creada" % p[3])
    else:
        variables[p[3]] = p[7][1]
        p[0] = (p[1], p[7][1], p[3],p[7])


def p_statement_create_empty(p):
    '''
    statement : Var Space NAME
    '''
    p[0] = (p[1], None, p[3])
    variables[p[3]] = None
    print(variables)

# Gramatica de una expresion
def p_statement_expr(p):
    '''
    statement : expression
    '''
    p[0] = p[1]
    if p[0] == None:
        return
    else:
        print(p[1][1])

def p_expression_Number(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = ('exp',p[1])

def p_expression_Function(p):
    '''expression : function
    '''
    p[0] = p[1]

def p_expression_name(p):
    """expression : NAME"""
    try:
        p[0] = ('exp',variables[p[1]])
    except LookupError:# arreglaaaaaaaaaaaaaaar
        print("Variable no definida '%s'" % p[1])
        p[0]='fabian busque que hacer aqui, att: wajo'

def p_operaciones(p):
    '''
    operaciones : expression Space expression
                '''
    p[0] = (p[1][1],p[3][1])

def p_Op_operaciones(p):
    '''
        operaciones : expression Space operaciones'''
    p[0] = (p[1][1], p[3])

def p_funciones(p):
    '''
    funciones : statement Coma Space statement
                | statement Coma Space funciones
    '''

    p[0] = (p[1],p[4])

# funcion para sumar los digitos de una tupla
def suma(tupla):
    suma1=0
    while (type(tupla[1]) == tuple):
        suma1 += tupla[0]
        tupla = tupla[1]
    return suma1 + tupla[0] + tupla[1]

#(Nombre, Resultado, tupla de valores)
def p_suma(p):
    '''
    function : Suma Space operaciones
    '''
    a= suma(p[3])
    p[0] = (p[1],a,p[3])

def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    try:
        variables[p[3]] = variables[p[3]] + 1
        p[0] = (p[1], p[3],variables[p[3]])
    except LookupError:
            print("La variable que desea incrementar no ha sido declarada")

def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    variables[p[3]] = variables[p[3]] * p[5][1] #preguntar al profe
    p[0] = (p[1], variables[p[3]], p[3],p[5][1])

# funcion de numero aleatorio
def p_Azar(p):
    '''function : Azar Space expression'''
    num = random.randint(0,p[3][1])
    p[0]= (p[1],num,p[3][1])

# funcion para cambiar de signo
def p_Menos(p):
    '''function :  Menos Space expression'''
    num = -p[3][1]
    p[0]=(p[1],num,p[3][1])

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
    print(p[3])
    p[0]=(p[1],producto(p[3]),p[3][1])

# funcion para calcular potencia y gramatica
def p_Potencia(p):
    '''function :  Potencia Space expression Space expression'''
    num = p[3][1]**p[5][1]
    p[0]=(p[1],num,p[3][1],p[5][1])

def p_Division(p):
    '''function :  Division Space expression Space expression'''
    num = p[3][1]/p[5][1]
    p[0]=(p[1],num,p[3][1],p[5][1])

def p_Resto(p):
    '''function :  Resto Space expression Space expression'''
    num = p[3][1]%p[5][1]
    p[0]=(p[1],num,p[3][1],p[5][1])

def p_RC(p):
    '''function :  RC Space expression'''
    num = m.sqrt(p[3][1])
    p[0]=(p[1],num,p[3][1])

def p_Sen(p):
    '''function :  Sen Space expression'''
    num = m.sin(m.radians(p[3][1]))
    p[0]=(p[1],num,p[3][1])

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
    p[0]=(p[1],Lista[num],Lista)

def p_Cuenta(p):
    '''function : Cuenta Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=(p[1],len(Lista),Lista)

def p_Ultimo(p):
    '''function : Ultimo Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=(p[1],Lista[len(Lista)-1],Lista)

def p_Elemento(p):
    '''function : Elemento Space expression Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[6])
    p[0]=(p[1],Lista[p[3][1]-1],Lista,p[3]) #(nombre,resultado,lista,indice)

def p_Primero(p):
    '''function : Pri Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista= makeList(p[4])
    p[0]=(p[1],Lista[0],Lista)

def p_Avanza(p):
    """
    function : Avanza Space expression
             | Avanza Space function
    """
    p[0] = (p[1], p[3][1])
    print("Avanza '%d' unidades" %p[0][1])

def p_Retrocede(p):
    """
    function : Retrocede Space expression
             | Retrocede Space function
    """
    p[0] = (p[1], p[3][1])
    print("Retrocede '%d' unidades" %p[0][1])

def p_GiraDerecha(p):
    """
    function : GiraDerecha Space expression
    """
    p[0] = (p[1], p[3][1])
    print("Gira '%d' grados a la derecha" %p[0][1])

def p_GiraIzquierda(p):
    """
    function : GiraIzquierda Space expression
    """
    p[0] = (p[1], p[3][1])
    print("Gira '%d' grados a la izquierda" %p[0][1])

def p_OcultaTortuga(p):
    """
    function : OcultaTortuga
    """
    p[0] = (p[1],None)
    print("Se oculta la tortuga")

def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    p[0] = (p[1],None)
    print("Aparece la Tortuga")

def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    a = [p[4][1],p[6][1]]
    p[0] = (p[1],a,p[4][1],p[6][1])

def p_PonRumbo(p):
    """
    function : PonRumbo Space expression
    """
    p[0] = (p[1], p[3][1])
    print("Tortuga en rumbo hacia los '%d' grados" %p[0][1])

def p_Rumbo(p):
    """
    function : Rumbo
    """
    p[0] = (p[1],None)
    print("Indicar el rumbo de la tortura")

def p_PonX(p):
    """
    function : PonX Space expression
    """
    p[0] = (p[1],p[3][1])
    print("Tortuga en la posicionX '%d'"%p[0][1])

def p_PonY(p):
    """
    function : PonY Space expression
    """
    p[0] = (p[1],p[3][1])
    print("Tortuga en la posicionY '%d'" % p[0][1])

def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    p[0] = (p[1],None)
    print("Comienza a dibujar")

def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    p[0] = (p[1],None)
    print("Levanta el lapiz y detiene el dibujo")

def p_Borrapantalla(p):
    """function : Borrapantalla"""
    p[0] = (p[1],None)

# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    '''function :  PonColorLapiz'''
    p[0] = (p[1],None)

# Funcion para poner la tortuga en el centro
def p_Centro(p):
    '''function :  Centro'''
    p[0] = (p[1],None)

# Funcion para pausar la ejecucion
def p_Espera(p):
    '''function :  Espera Space expression'''
    time.sleep(p[3][1]/60)
    p[0] = (p[1],p[3][1])
    print("Wait de " + str(p[3][1]/60) + " segundos")


# Funcion que ejecuta las Ordenes
def p_Ejecuta(p):
    '''function :  Ejecuta Space LeftSquareBracket operaciones RightSquareBracket'''
    p[0] = (p[1],p[4])

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
    p[0] = (p[1],a,p[3])

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
    res= y((p[3][1],p[4][1]))
    p[0] = (p[1],res,p[3],p[4])
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
    a= O((p[3][1],p[4][1]))
    p[0] = (p[1], a, p[3], p[4])

# Funcion que devuelve CIERTO si n > n1
def MayorQue(num1,num2):
    if(num1 > num2):
        return "CIERTO"
    else:
        return "FALSO"

def p_MayorQue(p):
    '''
    function : MayorQue Space expression PuntoComa Space expression
    '''
    a= MayorQue(p[3][1],p[6][1])
    p[0] = (p[1], a, p[3])

# Funcion que devuelve Falso si n < n1
def MenorQue(num1,num2):
    if(num1 < num2):
        return "CIERTO"
    else:
        return "FALSO"

def p_MenorQue(p):
    '''
    function : MenorQue Space expression PuntoComa Space expression
    '''
    a= MenorQue(p[3][1],p[6][1])
    p[0] = (p[1], a, p[3])

# Funcion que redondea un numero
def p_Redondea(p):
    '''
        function : Redondea Space expression
    '''
    p[0] = (p[1], round(p[3][1]), p[3])

# Funcion que calcula el coseno de un numero
def p_Cos(p):
    '''function :  Cos Space expression'''
    num = m.cos(m.radians(p[3][1]))
    p[0] = (p[1], num, p[3][1])

# Funcion para restar los digitos de una tupla
def restar(tupla):
    resta=0
    while (type(tupla[1]) == tuple):
        resta = tupla[0] - tupla[1][0]
        tupla = (resta,tupla[1][1])
    return tupla[0] - tupla[1]

def p_restar(p):
    '''
    function : Diferencia Space operaciones
    '''
    a = restar(p[3])
    p[0] = (p[1], a, p[3])

def repite(tupla):
    can_veces= tupla[0]-1
    global Entrada
    while Entrada[0]!="[":
        Entrada=Entrada[1:]
    Entrada = Entrada[1:-1]
    Entrada = Entrada.split(",")
    while can_veces!=0:
        s=Entrada[0]
        parser.parse(s)
        num=1
        while len(Entrada)!=num:
            s = Entrada[num][1:]
            print(s)
            num+=1
            parser.parse(s)
        can_veces-=1

# Ejecuta si se cumple la condicion
def p_Si(p):
    '''function :  Si Space  expression LeftSquareBracket function RightSquareBracket
                | Si Space expression LeftSquareBracket funciones RightSquareBracket
    '''
    p[0] = (p[1],p[3],p[5])
    if(p[0][1][1] == 'CIERTO'):
        print("EJECUTA")
        repite((2,None))
    else:
        print("NO EJECUTA")


# Funcion que repite ordenes cierta cantidad de veces
def p_Repite(p):# Repite 2[Inic a = Suma a 1, Avanza a] hacer que acepte esto..........................
    '''
    function : Repite Space expression LeftSquareBracket funciones RightSquareBracket
            | Repite Space expression LeftSquareBracket  statement RightSquareBracket
    '''
    p[0] = (p[3][1],p[5])
    repite(p[0])


# Retorna error de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis de '%s'" % p.value)
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

while True:
    global Entrada
    try:
        s = input('->')
        Entrada = s
    except EOFError:
        break
    if not s:continue
    parser.parse(s)


