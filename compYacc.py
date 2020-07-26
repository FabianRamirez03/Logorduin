import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys

global Entrada, Funcion, toDo, rumbo,Error, listaEjecuta,Comentario, Repite
listaEjecuta = []
Error = ""
Funcion = False
Comentario = False
Repite = True
coloresPermitidos = ["blanco", "azul", "marron", "cian", "gris", "amarillo", "negro", "rojo", "verde"]
ListaFunciones = {}
Instrucciones = {}
variables = {}

#Gramatica de asignacion de variables
def p_statement_create(p):
    """
    statement : Var Space NAME Space EQUALS Space expression
    """
    global Error
    if p[3] not in variables:
        p[0] = (p[1], p[7][1], p[3])
        variables[p[3]] = p[7][1]
    else:
        global toDo
        Error = str("La variable '%s' ya fue creada" % p[3])
        toDo = "Logic"

#Gramatica de variable vacia
def p_statement_create_empty(p):
    """
    statement : Var Space NAME
    """
    global Funcion, Entrada, Error
    if p[3] not in variables:
        p[0] = (p[1], 0, p[3])
        variables[p[3]] = 0
    else:
        Error = str("La variable '%s' ya fue creada" % p[3])

def p_comment(p):
    """
    statement : Comentario
    """
    global Comentario
    Comentario = True

#Inicializacion de una variable
def p_statement_assign(p):
    """
    function : Inic Space NAME Space EQUALS Space expression
             | Inic Space NAME Space EQUALS Space function
    """
    global Funcion, Entrada, Error
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        if p[3] not in variables:
            Error = str("La variable '%s' no ha sido creada" % p[3])
        else:
            variables[p[3]] = p[7][1]
            p[0] = (p[1], p[7][1], p[3], p[7])

# Gramatica de una expresion
def p_statement_expr(p):
    """
    statement : expression
    """
    p[0] = p[1]
    if p[0] == None:
        return
    else:
        global Funcion, Entrada,toDo, Repite
        if (Funcion):
                for elemento in Instrucciones:
                    ultimoElemento = elemento
                Instrucciones[ultimoElemento][1] += [Entrada]
        else:
            toDo = "printConsola(text="+str(p[1][1])+")"
#Expression acepta numeros
def p_expression_Number(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = ('exp',p[1])

#Expression acepta funciones
def p_expression_Function(p):
    """
    expression : function
    """
    p[0] = p[1]

#Expression puede ser un nombre
def p_expression_name(p):
    """
    expression : NAME
    """
    global Error
    try:
        p[0] = ('exp', variables[p[1]])
    except LookupError:
        Error = str("Variable no definida '%s'" % p[1])


#Sintaxis de operaciones
def p_operaciones(p):
    """
    operaciones : expression Space expression
    """
    p[0] = (p[1][1],p[3][1])


def p_Op_operaciones(p):
    """
    operaciones : expression Space operaciones
    """
    p[0] = (p[1][1], p[3])


def p_funciones(p):
    """
    funciones : statement Coma Space statement
              | statement Coma Space funciones
    """
    p[0] = (p[1],p[4])


# funcion para sumar los digitos de una tupla
def suma(tupla):
    suma1 = 0
    while (type(tupla[1]) == tuple):
        suma1 += tupla[0]
        tupla = tupla[1]
    return suma1 + tupla[0] + tupla[1]


# (Nombre, Resultado, tupla de valores)
def p_suma(p):
    """
    function : Suma Space operaciones
    """
    a = suma(p[3])
    p[0] = (p[1],a,p[3])

#Funcion que incrementa en 1 el valor de una variable
def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    global Error
    try:
        variables[p[3]] = variables[p[3]] + 1
        p[0] = (p[1], p[3],variables[p[3]])
    except LookupError:
            Error = str("La variable '%s' que desea incrementar no ha sido declarada previamente" %p[3])

#Funcion que incrementa el valor de una variable N veces
def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    global Error
    try:
        variables[p[3]] = variables[p[3]] * p[5][1]
        p[0] = (p[1], variables[p[3]], p[3],p[5][1])
    except LookupError:
            Error = str("La variable '%s' que desea incrementar no ha sido declarada previamente" %p[3])


# funcion de numero aleatorio
def p_Azar(p):
    """
    function : Azar Space expression
    """
    num = random.randint(0,p[3][1])
    p[0]= (p[1],num,p[3][1])

# funcion para cambiar de signo
def p_Menos(p):
    """
    function :  Menos Space expression
    """
    num = -p[3][1]
    p[0]=(p[1],num,p[3][1])

# funcion para multiplicar los digitos de una tupla
def producto(tupla):
    num = 1
    while (type(tupla[1]) == tuple):
        num *= tupla[0]
        tupla = tupla[1]
    return num * tupla[0] * tupla[1]

#Gramatica de la multiplicacion
def p_producto(p):
    """
    function : Producto Space operaciones
    """
    p[0]=(p[1],producto(p[3]),p[3][1])

# funcion para calcular potencia y gramatica
def p_Potencia(p):
    """
    function :  Potencia Space expression Space expression
    """
    num = p[3][1]**p[5][1]
    p[0]=(p[1],num,p[3][1],p[5][1])

def p_Division(p):
    """
    function :  Division Space expression Space expression
    """
    global Error
    num = p[3][1]
    denom = p[5][1]
    if denom == 0:
        Error = ("Error, no se puede dividir entre 0")
    else:
        resultado = num / denom
        p[0]=(p[1],resultado,num,denom)

def p_Resto(p):
    """
    function :  Resto Space expression Space expression
    """
    global Error
    if p[5][1] != 0:
        num = p[3][1]%p[5][1]
        p[0]=(p[1],num,p[3][1],p[5][1])
    else:
        Error = str("Error, no se puede hacer el residuo de 0")

def p_RC(p):
    """
    function :  RC Space expression
    """
    num = m.sqrt(p[3][1])
    p[0] = (p[1], num, p[3][1])

def p_Sen(p):
    """
    function :  Sen Space expression
    """
    num = m.sin(m.radians(p[3][1]))
    p[0] = (p[1], num, p[3][1])

def makeList(tupla):
    lista=[]
    while(type(tupla[1]) == tuple):
        lista+=[tupla[0]]
        tupla=tupla[1]
    return lista+[tupla[0]]+[tupla[1]]

def p_Elegir(p):
    """
    function : Elegir Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista= makeList(p[4])
    num= random.randint(0,len(Lista)-1)
    p[0]=(p[1],Lista[num],Lista)

def p_Cuenta(p):
    """
    function : Cuenta Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista= makeList(p[4])
    p[0]=(p[1],len(Lista),Lista)

def p_Ultimo(p):
    """
    function : Ultimo Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista= makeList(p[4])
    p[0]=(p[1],Lista[len(Lista)-1],Lista)

def p_Elemento(p):
    """
    function : Elemento Space expression Space LeftSquareBracket operaciones RightSquareBracket
    """
    global Error
    Lista = makeList(p[6])
    if (p[3] <= len[Lista]):
        p[0] = (p[1],Lista[p[3][1]-1],Lista,p[3])
    else:
        Error = str("El indice que desea acceder esta fuera de rango")

def p_Primero(p):
    """
    function : Pri Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista = makeList(p[4])
    p[0]=(p[1],Lista[0],Lista)

def p_Avanza(p):
    """
    function : Avanza Space expression
             | Avanza Space function
    """
    global toDo
    p[0] = (p[1], p[3][1])
    distance = str(p[0][1])
    print("Avanza '%d' unidades" % p[0][1])
    toDo = "Avanza(distance = " + str(distance) + ")"

def p_Retrocede(p):
    """
    function : Retrocede Space expression
             | Retrocede Space function
    """
    global toDo
    p[0] = (p[1], p[3][1])
    distance = p[0][1]
    print("Retrocede '%d' unidades" %p[0][1])
    toDo = "Retroceder(distance = " + str(distance) + ")"

def p_GiraDerecha(p):
    """
    function : GiraDerecha Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    grades = p[0][1]
    print("Gira '%d' grados a la derecha" % p[0][1])
    toDo = "giraDerecha(grades =" + str(grades) + ")"

def p_GiraIzquierda(p):
    """
    function : GiraIzquierda Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    grades = p[0][1]
    print("Gira '%d' grados a la izquierda" % p[0][1])
    toDo = "giraIzquierda(grades =" + str(grades) + ")"

def p_OcultaTortuga(p):
    """
    function : OcultaTortuga
    """
    global toDo
    p[0] = (p[1],None)
    print("Se oculta la tortuga")
    toDo = "ocultaTortuga()"

def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    global toDo
    p[0] = (p[1],None)
    print("Aparece la Tortuga")
    toDo = "apareceTortuga()"

def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    global toDo
    a = [p[4][1],p[6][1]]
    p[0] = (p[1],a,p[4][1],p[6][1])
    posx = p[4][1]
    posy = p[6][1]
    toDo = "ponpos( coords = [" + str(posx) + "," + str(posy) + "] )"
    print(str(posx) + " " + str(posy))

def p_PonRumbo(p):
    """
    function : PonRumbo Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    print("Tortuga en rumbo hacia los '%d' grados" % p[0][1])
    rumbo = p[0][1]
    toDo = "Ponrumbo(grades = " + str(rumbo) + ")"

def p_Rumbo(p):
    """
    function : Rumbo
    """
    global toDo
    p[0] = (p[1],None)
    print("Indicar el rumbo de la tortura")

def p_PonX(p):
    """
    function : PonX Space expression
    """
    global toDo
    p[0] = (p[1],p[3][1])
    xPos = p[0][1]
    print("Tortuga en la posicionX '%d'" % p[0][1])
    toDo = "ponx(xCoord = " + str(xPos) + ")"

def p_PonY(p):
    """
    function : PonY Space expression
    """
    global toDo
    p[0] = (p[1],p[3][1])
    yPos = p[0][1]
    print("Tortuga en la posicionY '%d'" % p[0][1])
    toDo = "pony(yCoord = " + str(yPos) + ")"

def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    global toDo
    p[0] = (p[1],None)
    print("Comienza a dibujar")
    toDo = "BajaLapiz()"

def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    global toDo
    p[0] = (p[1],None)
    print("Levanta el lapiz y detiene el dibujo")
    toDo = "subeLapiz()"

def p_Borrapantalla(p):
    """function : Borrapantalla"""
    global toDo
    p[0] = (p[1],None)
    toDo = "clean_canvas()"

# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    """
    function :  PonColorLapiz Space NAME
    """
    global toDo
    global Error
    color = p[3]
    if color not in coloresPermitidos:
        Error = str("Error, el color " + color + " no es un color permitido")
    else:
        p[0] = (p[1],p[3])
        strColor = p[3]
        toDo = "PonColorLapiz(color = '" + strColor + "')"

# Funcion para poner la tortuga en el centro
def p_Centro(p):
    """
    function :  Centro
    """
    global toDo
    p[0] = (p[1],None)
    toDo = "centro()"

# Funcion para pausar la ejecucion
def p_Espera(p):
    """
    function :  Espera Space expression
    """
    global toDo
    p[0] = (p[1],p[3][1])
    segs = p[3][1]
    print("Wait de " + str(p[3][1] / 60) + " segundos")
    toDo = "espera(seg = " + str(segs) + ")"


def Var_Array(tupla):
    listaFinal = []
    for x in tupla:
        if isinstance(x,tuple):
            listaFinal.append(x[1])
        else:
            listaFinal.append(tupla[-1])
            break
    return listaFinal

def p_Ejecuta_Parametro(p):
    """
    function : Ejecuta Space NAME Space LeftSquareBracket Variables RightSquareBracket
    """
    global Error, listaEjecuta, toDo
    listaEjecuta = []
    parametros = Var_Array(makeList(p[6]))
    nombre = p[3]
    if nombre not in Instrucciones:
        Error = str("No existe la funcion de nombre " + nombre)
    else:
        for elemento in Instrucciones:
            if elemento == nombre:
                if len(parametros) != len(Instrucciones[elemento][0]):
                    Error = str("La cantidad de parametros ingresados no coincide con la cantidad de variables de la funcion")
                else:
                    Instrucciones[elemento][2] = parametros
            listaFinal =[]

            for i in range(0,len(Instrucciones[elemento][1])):
                string = Instrucciones[elemento][1][i]
                temp = Instrucciones[elemento][1][i].split(" ")
                listaValores = []
                func = ""

                for j in temp:
                    if j in Instrucciones[elemento][0] and (temp[0] != "Inic" or j != temp[1]):
                        pos = Instrucciones[elemento][0].index(j)
                        valor = Instrucciones[elemento][2][pos]
                        listaValores.append(str(valor))
                    else:
                        listaValores.append(j)
                for g in listaValores:
                    if listaValores.index(g) == 0:
                        func += g
                    else:
                        func += " " + g
                if temp[0] != "Repite":
                    listaFinal.append(func)
                else:
                    listaFinal.append(func)
                    break
        for inst in listaFinal:
            parser.parse(inst)
            print(inst)
            listaEjecuta.append(toDo)
        a = toDo
        b = listaEjecuta
        toDo = listaEjecuta


# Funcion que ejecuta las Ordenes
def p_Ejecuta_Funcion(p):
    """
    function :  Ejecuta Space NAME
    """
    global Error
    nombre = p[3]
    if nombre not in Instrucciones:
        Error = str("No existe la funcion de nombre " + nombre)
    else:
        for elemento in Instrucciones:
            if elemento == nombre:
                for instruccion in Instrucciones[elemento][1]:
                    parser.parse(instruccion)

def p_Ejecuta_Ordenes(p):
    """
    function : Ejecuta Space LeftSquareBracket Variables RightSquareBracket
    """
    lista = makeList(p[4])
    listaFinal = []
    for elemento in lista:
        if isinstance(elemento, tuple):
            listaFinal.append(str(elemento[0]) + " " + str(elemento[1]))
        else:
            listaFinal.append(str(lista[lista.index(elemento)]) + " " + str(lista[lista.index(elemento ) + 1]))
            break
    for x in listaFinal:
        parser.parse(x)

#Reinicia el compilador
def reiniciar():
    global Entrada, Funcion, toDo, Error, listaEjecuta, Comentario,variables, Instrucciones, ListaFunciones, Repite
    variables = {}
    Instrucciones = {}
    ListaFunciones = {}
    Entrada = ""
    Error = ""
    Comentario = False
    Funcion = False
    listaEjecuta = []
    toDo = ""
    Repite = True


# Funcion que devuelve True si la dos numeros son iguales
def iguales(tupla):
    if (tupla[0] == tupla[1]):
        return "CIERTO"
    else:
        return "FALSO"

def p_iguales(p):
    """
    function : Iguales Space operaciones
    """
    a= iguales(p[3])
    p[0] = (p[1],a,p[3])

# Funcion que devuelve CIERTO si dos condiciones se cumplen
def y(tupla):
    if (tupla[0] == "CIERTO" and tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"

def p_Y(p):
    """
    function : Y Space function function
    """
    res= y((p[3][1],p[4][1]))
    p[0] = (p[1],res,p[3],p[4])
    print(p[0])


# Funcion que devuelve CIERTO si al menos una condicion se cumple
def O(tupla):
    if (tupla[0] == "CIERTO" or tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"

def p_O(p):
    """
    function : O Space function function
    """
    a= O((p[3][1],p[4][1]))
    p[0] = (p[1], a, p[3], p[4])

# Funcion que devuelve CIERTO si n > n1
def MayorQue(num1, num2):
    if (num1 > num2):
        return "CIERTO"
    else:
        return "FALSO"

def p_MayorQue(p):
    """
    function : MayorQue Space expression PuntoComa Space expression
    """
    a = MayorQue(p[3][1],p[6][1])
    p[0] = (p[1], a, p[3])

# Funcion que devuelve Falso si n < n1
def MenorQue(num1, num2):
    if (num1 < num2):
        return "CIERTO"
    else:
        return "FALSO"


def p_MenorQue(p):
    """
    function : MenorQue Space expression PuntoComa Space expression
    """
    a = MenorQue(p[3][1],p[6][1])
    p[0] = (p[1], a, p[3])

# Funcion que redondea un numero
def p_Redondea(p):
    """
    function : Redondea Space expression
    """
    p[0] = (p[1], round(p[3][1]), p[3])


# Funcion que calcula el coseno de un numero
def p_Cos(p):
    """
    function :  Cos Space expression
    """
    num = m.cos(m.radians(p[3][1]))
    p[0] = (p[1], num, p[3][1])

#Funcion para restar los digitos de una tupla
def restar(tupla):
    while (type(tupla[1]) == tuple):
        resta = tupla[0] - tupla[1][0]
        tupla = (resta, tupla[1][1])
    return tupla[0] - tupla[1]


def p_restar(p):
    """
    function : Diferencia Space operaciones
    """
    a = restar(p[3])
    p[0] = (p[1], a, p[3])

def repite(tupla):
    can_veces = tupla[0]
    global Entrada, listaEjecuta, toDo, Repite
    Repite = False
    print(str(Entrada) + str(tupla) + "ESTA MIERDA")
    while Entrada[0] != "[":
        Entrada = Entrada[1:]
    Entrada = Entrada[1:-1]
    Entrada = Entrada.split(",")
    aaa = Entrada
    while can_veces != 0:
        s = Entrada[0]
        parser.parse(s)
        listaEjecuta.append(toDo)
        num = 1
        while len(Entrada) != num:
            s = Entrada[num][1:]
            print(s)
            num += 1
            parser.parse(s)
            string = toDo
            listaEjecuta.append(toDo)
        toDo = listaEjecuta
        can_veces -= 1
    Repite = True


# Ejecuta si se cumple la condicion
def p_Si(p):
    """
    function : Si Space  expression LeftSquareBracket function RightSquareBracket
             | Si Space expression LeftSquareBracket funciones RightSquareBracket
    """
    p[0] = (p[1],p[3],p[5])
    if(p[0][1][1] == 'CIERTO'):
        print("EJECUTA")
        repite((2, None))
    else:
        print("NO EJECUTA")

# Funcion que repite ordenes N cantidad de veces
def p_Repite(p):
    """
    function : Repite Space expression Space LeftSquareBracket funciones RightSquareBracket
             | Repite Space expression Space LeftSquareBracket  statement RightSquareBracket
    """
    p[0] = (p[3][1],p[5])
    repite(p[0])

#Acepta nombres de variables
def p_Variable(p):
    """
    Variable : NAME Coma Space NAME
             | NAME Coma Space Variable
    """
    p[0] = (p[1],p[4])

#Acepta nombres y funciones para variables
def p_Variables(p):
    """
    Variables : expression
              | expression Coma Space Variables
    """
    if len(p) > 2:
        p[0] = (p[1],p[4])
    else:
        p[0]=(p[1])

#Detecta el fin de una funcion
def p_Fin(p):
    """
    function : Fin
    """
    global Funcion
    Funcion = False
    print(Instrucciones)

#Gramatica para creacion de una funcion sin variables
def p_ParaSin(p):
    """
    function : Para Space NAME Space LeftSquareBracket RightSquareBracket
    """
    global Funcion,Error

    if Funcion == True:
        Error = str("Error no puede crear un 'Para' dentro de otro")
    else:
        Funcion = True
        if p[3] not in Instrucciones:
            Instrucciones[p[3]] = [[None], []]
            print(Instrucciones)
        else:
            Error = str("La funcion con nombre '%s' ya fue creada" % p[3])

#Gramatica para la creacion de una funcion con una variable
def p_ParaUna(p):
    """
    function : Para Space NAME Space LeftSquareBracket NAME RightSquareBracket
    """
    global Funcion,Error
    variable = "Var " + p[6]
    if Funcion == True:
        Error = str("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True
        parser.parse(variable)
        if p[3] not in Instrucciones:
            Instrucciones[p[3]] = [p[6], [], []]
            print(Instrucciones)
        else:
            Error = str("La funcion con nombre '%s' ya fue creada" % p[3])

#Gramatica para la creacion de una funcion con variables
def p_ParaVarias(p):
    """
    function : Para Space NAME Space LeftSquareBracket Variable RightSquareBracket
    """
    global Funcion,Error
    variable = makeList(p[6])
    if Funcion == True:
        Error = str("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True
        for var in variable:
            parser.parse("Var " + str(var))
        if p[3] not in Instrucciones:
            var = makeList(p[6])
            Instrucciones[p[3]] = [var, [], []]
            print(Instrucciones)
        else:
            Error = str("La funcion con nombre '%s' ya fue creada" % p[3])


# Retorna error de sintaxis
def p_error(p):
    global Error
    if p:
        Error = str("Error de sintaxis en '%s'" % p.value)
        raise Exception()
    else:
        Error = str("Error de sintaxis")
        raise Exception()


parser = yacc.yacc()
"""
while not Error:
    global Entrada
    s = input('->')
    Entrada = s
    if not s:
        continue
    try:
        parser.parse(s)
    except Exception as e:
        if not Error:
            Error = str(e)
print(Error)
"""
#Hacer la documentacion
#Errores del dia
#Arreglar el si
#Arreglar repite en para
