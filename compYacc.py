import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys

global Entrada, toDo, rumbo
global Funcion
Funcion = False
ListaFunciones = {}
Instrucciones = {}
variables = {}
toDo = ""


# Gramatica de asignacion de variables
def p_statement_create(p):
    '''
    statement : Var Space NAME Space EQUALS Space expression
    '''
    if p[3] not in variables:
        p[0] = (p[1], p[7][1], p[3])
        variables[p[3]] = p[7][1]
        print(p[0])
        print(variables)
    else:
        global toDo
        print("La variable '%s' ya fue creada" % p[3])
        toDo = "Logic"


def p_statement_assign(p):
    """
    function : Inic Space NAME Space EQUALS Space expression
             | Inic Space NAME Space EQUALS Space function
    """
    if p[3] not in variables:
        print("La variable '%s' no ha sido creada" % p[3])
    else:
        global toDo
        variables[p[3]] = p[7][1]
        p[0] = (p[1], p[7][1], p[3], p[7])
        toDo = "Logic"


def p_statement_create_empty(p):
    '''
    statement : Var Space NAME
    '''
    p[0] = (p[1], 0, p[3])
    variables[p[3]] = 0
    print(variables)
    global toDo
    toDo = "Logic"


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
    p[0] = ('exp', p[1])


def p_expression_Function(p):
    '''expression : function
    '''
    p[0] = p[1]


def p_expression_name(p):
    """expression : NAME"""
    try:
        p[0] = ('exp', variables[p[1]])
    except LookupError:  # arreglaaaaaaaaaaaaaaar
        print("Variable no definida '%s'" % p[1])
        raise Exception()


def p_operaciones(p):
    '''
    operaciones : expression Space expression
                '''
    p[0] = (p[1][1], p[3][1])


def p_Op_operaciones(p):
    '''
        operaciones : expression Space operaciones'''
    p[0] = (p[1][1], p[3])


def p_funciones(p):
    '''
    funciones : statement Coma Space statement
                | statement Coma Space funciones
    '''

    p[0] = (p[1], p[4])


# funcion para sumar los digitos de una tupla
def suma(tupla):
    suma1 = 0
    while (type(tupla[1]) == tuple):
        suma1 += tupla[0]
        tupla = tupla[1]
    return suma1 + tupla[0] + tupla[1]


# (Nombre, Resultado, tupla de valores)
def p_suma(p):
    '''
    function : Suma Space operaciones
    '''
    a = suma(p[3])
    p[0] = (p[1], a, p[3])


def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    try:
        variables[p[3]] = variables[p[3]] + 1
        p[0] = (p[1], p[3], variables[p[3]])
        global toDo
        toDo = "Logic"
    except LookupError:
        print("La variable que desea incrementar no ha sido declarada")


def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    variables[p[3]] = variables[p[3]] * p[5][1]  # preguntar al profe
    p[0] = (p[1], variables[p[3]], p[3], p[5][1])


# funcion de numero aleatorio
def p_Azar(p):
    '''function : Azar Space expression'''
    num = random.randint(0, p[3][1])
    p[0] = (p[1], num, p[3][1])


# funcion para cambiar de signo
def p_Menos(p):
    '''function :  Menos Space expression'''
    num = -p[3][1]
    p[0] = (p[1], num, p[3][1])


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
    p[0] = (p[1], producto(p[3]), p[3][1])


# funcion para calcular potencia y gramatica
def p_Potencia(p):
    '''function :  Potencia Space expression Space expression'''
    num = p[3][1] ** p[5][1]
    p[0] = (p[1], num, p[3][1], p[5][1])


def p_Division(p):
    '''function :  Division Space expression Space expression'''
    num = p[3][1]
    denom = p[5][1]
    if denom == 0:
        print("Error, no se puede dividir entre cero")
    else:
        resultado = num / denom
        p[0] = (p[1], resultado, num, denom)


def p_Resto(p):
    '''function :  Resto Space expression Space expression'''
    num = p[3][1] % p[5][1]
    p[0] = (p[1], num, p[3][1], p[5][1])


def p_RC(p):
    '''function :  RC Space expression'''
    num = m.sqrt(p[3][1])
    p[0] = (p[1], num, p[3][1])


def p_Sen(p):
    '''function :  Sen Space expression'''
    num = m.sin(m.radians(p[3][1]))
    p[0] = (p[1], num, p[3][1])


def makeList(tupla):
    lista = []
    print(tupla)
    while (type(tupla[1]) == tuple):
        lista += [tupla[0]]
        tupla = tupla[1]
    return lista + [tupla[0]] + [tupla[1]]


def p_Elegir(p):
    '''function : Elegir Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista = makeList(p[4])
    num = random.randint(0, len(Lista) - 1)
    p[0] = (p[1], Lista[num], Lista)


def p_Cuenta(p):
    '''function : Cuenta Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista = makeList(p[4])
    p[0] = (p[1], len(Lista), Lista)


def p_Ultimo(p):
    '''function : Ultimo Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista = makeList(p[4])
    p[0] = (p[1], Lista[len(Lista) - 1], Lista)


def p_Elemento(p):
    '''function : Elemento Space expression Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista = makeList(p[6])
    p[0] = (p[1], Lista[p[3][1] - 1], Lista, p[3])  # (nombre,resultado,lista,indice)


def p_Primero(p):
    '''function : Pri Space LeftSquareBracket operaciones RightSquareBracket'''
    Lista = makeList(p[4])
    p[0] = (p[1], Lista[0], Lista)


def p_Prueba(p):
    '''
    function : Prueba
    '''
    for elemento in Instrucciones:
        holi = elemento
    Instrucciones[holi][1] += ['avanza']
    Instrucciones[holi][1] += ['casa']


def p_Avanza(p):
    """
    function : Avanza Space expression
             | Avanza Space function
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Avanza '%d' unidades" % p[0][1])
        distance = p[0][1]
        toDo = "Avanza(distance = " + str(distance) + ")"


def p_Retrocede(p):
    """
    function : Retrocede Space expression
             | Retrocede Space function
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Retrocede '%d' unidades" % p[0][1])
        distance = p[0][1]
        toDo = "Retroceder(distance = " + str(distance) + ")"


def p_GiraDerecha(p):
    """
    function : GiraDerecha Space expression
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        grades = p[0][1]
        print("Gira '%d' grados a la derecha" % p[0][1])
        toDo = "giraDerecha(grades =" + str(grades) + ")"


def p_GiraIzquierda(p):
    """
    function : GiraIzquierda Space expression
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        grades = p[0][1]
        print("Gira '%d' grados a la izquierda" % p[0][1])
        toDo = "giraIzquierda(grades =" + str(grades) + ")"


def p_OcultaTortuga(p):
    """
    function : OcultaTortuga
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)
        print("Se oculta la tortuga")


def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)
        print("Aparece la Tortuga")


def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        a = [p[4][1], p[6][1]]
        p[0] = (p[1], a, p[4][1], p[6][1])
        posx = p[4][1]
        posy = p[6][1]
        toDo = "ponpos( coords = ["+str(posx)+","+str(posy)+"] )"
        print(str(posx) + " " + str(posy))


def p_PonRumbo(p):
    """
    function : PonRumbo Space expression
    """
    global Funcion, Entrada, toDo, rumbo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Tortuga en rumbo hacia los '%d' grados" % p[0][1])
        rumbo = p[0][1]
        toDo = "Ponrumbo(grades = " + str(rumbo) + ")"


def p_Rumbo(p):
    """
    function : Rumbo
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)
        print("El rumbo de la tortura es " + str(rumbo))


def p_PonX(p):
    """
    function : PonX Space expression
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        xPos = p[0][1]
        print("Tortuga en la posicionX '%d'" % p[0][1])
        toDo = "ponx(xCoord = " + str(xPos) + ")"


def p_PonY(p):
    """
    function : PonY Space expression
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        yPos = p[0][1]
        print("Tortuga en la posicionY '%d'" % p[0][1])
        toDo = "pony(yCoord = " + str(yPos) + ")"


def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    global Funcion, Entrada, toDo
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)
        print("Comienza a dibujar")
        toDo = "BajaLapiz()"


def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)
        print("Levanta el lapiz y detiene el dibujo")


def p_Borrapantalla(p):
    """function : Borrapantalla"""
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)


# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    '''function :  PonColorLapiz'''
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)


# Funcion para poner la tortuga en el centro
def p_Centro(p):
    '''function :  Centro'''
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        p[0] = (p[1], None)


# Funcion para pausar la ejecucion
def p_Espera(p):
    '''function :  Espera Space expression'''
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            holi = elemento
        Instrucciones[holi][1] += [Entrada]
    else:
        time.sleep(p[3][1] / 60)
        p[0] = (p[1], p[3][1])
        print("Wait de " + str(p[3][1] / 60) + " segundos")


# Funcion que ejecuta las Ordenes
def p_Ejecuta(p):
    '''function :  Ejecuta Space LeftSquareBracket operaciones RightSquareBracket'''
    p[0] = (p[1], p[4])


# Funcion que devuelve True si la dos numeros son iguales
def iguales(tupla):
    if (tupla[0] == tupla[1]):
        return "CIERTO"
    else:
        return "FALSO"


def p_iguales(p):
    '''
    function : Iguales Space operaciones
    '''
    a = iguales(p[3])
    p[0] = (p[1], a, p[3])


# Funcion que devuelve CIERTO si dos condiciones se cumplen
def y(tupla):
    if (tupla[0] == "CIERTO" and tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"


def p_Y(p):
    '''
    function : Y Space function function
    '''
    res = y((p[3][1], p[4][1]))
    p[0] = (p[1], res, p[3], p[4])
    print(p[0])


# Funcion que devuelve CIERTO si al menos una condicion se cumple
def O(tupla):
    if (tupla[0] == "CIERTO" or tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"


def p_O(p):
    '''
    function : O Space function function
    '''
    a = O((p[3][1], p[4][1]))
    p[0] = (p[1], a, p[3], p[4])


# Funcion que devuelve CIERTO si n > n1
def MayorQue(num1, num2):
    if (num1 > num2):
        return "CIERTO"
    else:
        return "FALSO"


def p_MayorQue(p):
    '''
    function : MayorQue Space expression PuntoComa Space expression
    '''
    a = MayorQue(p[3][1], p[6][1])
    p[0] = (p[1], a, p[3])


# Funcion que devuelve Falso si n < n1
def MenorQue(num1, num2):
    if (num1 < num2):
        return "CIERTO"
    else:
        return "FALSO"


def p_MenorQue(p):
    '''
    function : MenorQue Space expression PuntoComa Space expression
    '''
    a = MenorQue(p[3][1], p[6][1])
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
    resta = 0
    while (type(tupla[1]) == tuple):
        resta = tupla[0] - tupla[1][0]
        tupla = (resta, tupla[1][1])
    return tupla[0] - tupla[1]


def p_restar(p):
    '''
    function : Diferencia Space operaciones
    '''
    a = restar(p[3])
    p[0] = (p[1], a, p[3])


def repite(tupla):
    can_veces = tupla[0] - 1
    global Entrada
    while Entrada[0] != "[":
        Entrada = Entrada[1:]
    Entrada = Entrada[1:-1]
    Entrada = Entrada.split(",")
    while can_veces != 0:
        s = Entrada[0]
        parser.parse(s)
        num = 1
        while len(Entrada) != num:
            s = Entrada[num][1:]
            print(s)
            num += 1
            parser.parse(s)
        can_veces -= 1


# Ejecuta si se cumple la condicion
def p_Si(p):
    '''function :  Si Space  expression LeftSquareBracket function RightSquareBracket
                | Si Space expression LeftSquareBracket funciones RightSquareBracket
    '''
    p[0] = (p[1], p[3], p[5])
    if (p[0][1][1] == 'CIERTO'):
        print("EJECUTA")
        repite((2, None))
    else:
        print("NO EJECUTA")


# Funcion que repite ordenes N cantidad de veces
def p_Repite(p):
    '''
    function : Repite Space expression LeftSquareBracket funciones RightSquareBracket
             | Repite Space expression LeftSquareBracket  statement RightSquareBracket
    '''
    p[0] = (p[3][1], p[5])
    repite(p[0])


def p_Variable(p):
    '''
    Variable : NAME Coma Space NAME
             | NAME Coma Space Variable
    '''
    p[0] = (p[1], p[4])


# [[Para casa []],[Avanza 10], [GiraDerecha 90]]
def p_ParaSin(p):
    '''
    function : Para Space NAME Space LeftSquareBracket RightSquareBracket
    '''
    global Funcion
    if p[3] not in Instrucciones:
        Instrucciones[p[3]] = {"SinVariables"}
        Funcion = True
        print(Instrucciones)
    else:
        print("La variable '%s' ya fue creada" % p[3])


# [Para casa[largo], [Avanza largo], [GiraDerecha 90], [Avanza largo],[Fin]]
def p_ParaUna(p):
    '''
    function : Para Space NAME Space LeftSquareBracket NAME RightSquareBracket
    '''
    global Funcion
    if p[3] not in Instrucciones:
        Instrucciones[p[3]] = {p[6]: None}
        # llamar funcion que lee lineas
        print(Instrucciones)
        print(p[3])
        print(p[0])
    else:
        print("La funcion '%s' ya fue creada" % p[3])


def ValidarPara(array):
    try:
        if (array[-1] == "Fin"):
            for instruccion in array[1:-2]:
                print(instruccion)

    except:
        print("Funcion invalida")


def p_ParaVarias(p):
    '''
    function : Para Space NAME Space LeftSquareBracket Variable RightSquareBracket
    '''
    global Funcion
    if p[3] not in Instrucciones:
        variableList = makeList(p[6])
        Instrucciones[p[3]] = [variableList, []]
        Funcion = True
        print(Instrucciones)
    else:
        print("La variable '%s' ya fue creada" % p[3])


# Retorna error de sintaxis
def p_error(p):
    if p:
        print("Error de sintaxis de '%s'" % p.value)
        raise Exception()
    else:
        print("Syntax error at EOF")
        raise Exception()


parser = yacc.yacc()

"""
while True:
    global Entrada
    try:
        s = input('->')
        Entrada = s
    except:
        break
    if not s:
        continue
    try:
        parser.parse(s)
    except:
        print("ERROR DESCONOCIDO")
#Arreglar el manejo de errores
#Crear bien las funciones de Para Fin
#Todo_lo que tenga parser.parse hay que agregar try except  
#Asi debe llegar la instruccion: [Para casa[largo], [Avanza largo], [GiraDerecha 90], [Avanza largo]]
"""
