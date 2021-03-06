import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
from compLexx import lexError
import sys

global Entrada, Funcion, toDo, rumbo, Error, listaEjecuta, Comentario, Repite, can_Repites, lenPar
listaEjecuta = []
Error = ""
Funcion = False
Comentario = False
Repite = True
can_Repites = 0
lenPar = 0
coloresPermitidos = ["blanco", "azul", "marron", "cian", "gris", "amarillo", "negro", "rojo", "verde"]
ListaFunciones = {}
Instrucciones = {}
variables = {}


# Gramatica de asignacion de variables
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


# Gramatica de variable vacia
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


# Inicializacion de una variable
def p_statement_assign(p):
    """
    function : Inic Space NAME Space EQUALS Space expression
             | Inic Space NAME Space EQUALS Space function
    """
    global Funcion, Entrada, Error, Repite, toDo,Instrucciones, lenPar
    toDo = ""
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
    global Funcion, Entrada, toDo, Repite, lenPar
    if (Funcion and Repite):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        if "Para" not in Entrada and "//" not in Entrada:
            Instrucciones[ultimoElemento][lenPar][1] += [Entrada]
        else:
            pass
        Repite = False
    else:
        pass


# Expression acepta numeros
def p_expression_Number(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = ('exp', p[1])


# Expression acepta funciones
def p_expression_Function(p):
    """
    expression : function
    """
    p[0] = p[1]


# Expression puede ser un nombre
def p_expression_name(p):
    """
    expression : NAME
    """
    global Error, coloresPermitidos
    try:
        if (p[1] in coloresPermitidos):
            p[0] = ('exp',p[1])
        else:
            p[0] = ('exp', variables[p[1]])
    except LookupError:
        Error = str("Variable no definida '%s'" % p[1])


# Sintaxis de operaciones
def p_operaciones(p):
    """
    operaciones : expression Space expression
    """
    p[0] = (p[1][1], p[3][1])


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
    """
    function : Suma Space operaciones
    """
    a = suma(p[3])
    p[0] = (p[1], a, p[3])


# Funcion que incrementa en 1 el valor de una variable
def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    global Error
    try:
        variables[p[3]] = variables[p[3]] + 1
        p[0] = (p[1], p[3], variables[p[3]])
    except LookupError:
        Error = str("La variable '%s' que desea incrementar no ha sido declarada previamente" % p[3])


# Funcion que incrementa el valor de una variable N veces
def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    global Error
    try:
        variables[p[3]] = variables[p[3]] * p[5][1]
        p[0] = (p[1], variables[p[3]], p[3], p[5][1])
    except LookupError:
        Error = str("La variable '%s' que desea incrementar no ha sido declarada previamente" % p[3])


# funcion de numero aleatorio
def p_Azar(p):
    """
    function : Azar Space expression
    """
    num = random.randint(0, p[3][1])
    p[0] = (p[1], num, p[3][1])


# funcion para cambiar de signo
def p_Menos(p):
    """
    function :  Menos Space expression
    """
    num = -p[3][1]
    p[0] = (p[1], num, p[3][1])


# funcion para multiplicar los digitos de una tupla
def producto(tupla):
    num = 1
    while (type(tupla[1]) == tuple):
        num *= tupla[0]
        tupla = tupla[1]
    return num * tupla[0] * tupla[1]


# Gramatica de la multiplicacion
def p_producto(p):
    """
    function : Producto Space operaciones
    """
    p[0] = (p[1], producto(p[3]), p[3][1])


# funcion para calcular potencia y gramatica
def p_Potencia(p):
    """
    function :  Potencia Space expression Space expression
    """
    num = p[3][1] ** p[5][1]
    p[0] = (p[1], num, p[3][1], p[5][1])


def p_Division(p):
    """
    function :  Division Space expression Space expression
    """
    global Error
    num = p[3][1]
    denom = p[5][1]
    if not Funcion:
        if denom == 0:
            Error = ("Error, no se puede dividir entre 0")
        else:
            resultado = num / denom
            p[0] = (p[1], resultado, num, denom)
    else:
        p[0] = (p[1], 0, num, denom)

def p_Resto(p):
    """
    function :  Resto Space expression Space expression
    """
    global Error
    if p[5][1] != 0:
        num = p[3][1] % p[5][1]
        p[0] = (p[1], num, p[3][1], p[5][1])
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
    lista = []
    while (type(tupla[1]) == tuple):
        lista += [tupla[0]]
        tupla = tupla[1]
    return lista + [tupla[0]] + [tupla[1]]


def p_Elegir(p):
    """
    function : Elegir Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista = makeList(p[4])
    num = random.randint(0, len(Lista) - 1)
    p[0] = (p[1], Lista[num], Lista)


def p_Cuenta(p):
    """
    function : Cuenta Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista = makeList(p[4])
    p[0] = (p[1], len(Lista), Lista)


def p_Ultimo(p):
    """
    function : Ultimo Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista = makeList(p[4])
    p[0] = (p[1], Lista[len(Lista) - 1], Lista)


def p_Elemento(p):
    """
    function : Elemento Space expression Space LeftSquareBracket operaciones RightSquareBracket
    """
    global Error
    Lista = makeList(p[6])
    if (p[3][1] <= len(Lista)):
        p[0] = (p[1], Lista[p[3][1] - 1], Lista, p[3])
    else:
        Error = str("El indice que desea acceder esta fuera de rango")


def p_Primero(p):
    """
    function : Pri Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista = makeList(p[4])
    p[0] = (p[1], Lista[0], Lista)


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
    print("Retrocede '%d' unidades" % p[0][1])
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
    p[0] = (p[1], None)
    print("Se oculta la tortuga")
    toDo = "ocultaTortuga()"


def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    global toDo
    p[0] = (p[1], None)
    print("Aparece la Tortuga")
    toDo = "apareceTortuga()"


def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    global toDo
    a = [p[4][1], p[6][1]]
    p[0] = (p[1], a, p[4][1], p[6][1])
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
    p[0] = (p[1], None)
    print("Indicar el rumbo de la tortura")


def p_PonX(p):
    """
    function : PonX Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    xPos = p[0][1]
    print("Tortuga en la posicionX '%d'" % p[0][1])
    toDo = "ponx(xCoord = " + str(xPos) + ")"


def p_PonY(p):
    """
    function : PonY Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    yPos = p[0][1]
    print("Tortuga en la posicionY '%d'" % p[0][1])
    toDo = "pony(yCoord = " + str(yPos) + ")"


def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    global toDo
    p[0] = (p[1], None)
    print("Comienza a dibujar")
    toDo = "BajaLapiz()"


def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    global toDo
    p[0] = (p[1], None)
    print("Levanta el lapiz y detiene el dibujo")
    toDo = "subeLapiz()"


def p_Borrapantalla(p):
    """function : Borrapantalla"""
    global toDo
    p[0] = (p[1], None)
    toDo = "clean_canvas()"


# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    """
    function :  PonColorLapiz Space expression
    """
    global toDo
    global Error
    color = p[3][1]

    if color not in coloresPermitidos:
        Error = str("Error, el color " + color + " no es un color permitido")
    else:
        p[0] = (p[1], p[3])
        strColor = p[3][1]
        toDo = "PonColorLapiz(color = '" + strColor + "')"


# Funcion para poner la tortuga en el centro
def p_Centro(p):
    """
    function :  Centro
    """
    global toDo
    p[0] = (p[1], None)
    toDo = "centro()"


# Funcion para pausar la ejecucion
def p_Espera(p):
    """
    function :  Espera Space expression
    """
    global toDo
    p[0] = (p[1], p[3][1])
    segs = p[3][1]
    print("Wait de " + str(p[3][1] / 60) + " segundos")
    toDo = "espera(seg = " + str(segs) + ")"


def Var_Array(tupla):
    listaFinal = []
    for x in tupla:
        if isinstance(x, tuple):
            listaFinal.append(x[1])
        else:
            listaFinal.append(tupla[-1])
            break
    return listaFinal


def key_exists(elemento, key):
    try:
        elemento[key]
        return True
    except:
        return False
def duplicatedIndex(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def p_Ejecuta_Parametro(p):
    """
    function : Ejecuta Space NAME Space LeftSquareBracket Variables RightSquareBracket
    """
    global Error, listaEjecuta, toDo, Entrada, Funcion, Instrucciones
    InicioEjecuta= p[1]+' '+p[3]
    Ejecutar=True
    if InicioEjecuta != Entrada[:len(InicioEjecuta)]:
        Ejecutar =False
    if not Funcion and Ejecutar:
        parametros = Var_Array(makeList(p[6]))
        lenParametros = len(parametros)
        nombre = p[3]
        if nombre not in Instrucciones:
            Error = str("No existe la funcion de nombre " + nombre)
        else:
            if not key_exists(Instrucciones[nombre], lenParametros):
                Error = str("No existe la funcion de nombre " + nombre + " con " + str(lenParametros) + " parámetros")
            else:
                for elemento in Instrucciones:
                    if elemento == nombre:
                        if len(parametros) != len(Instrucciones[elemento][lenParametros][0]) and not isinstance(Instrucciones[elemento][lenParametros][0],str):
                            Error = str(
                                "La cantidad de parametros ingresados no coincide con la cantidad de variables de la funcion")
                        else:
                            Instrucciones[elemento][lenParametros][2] = parametros
                        listaFinal = []

                        for i in range(0, len(Instrucciones[elemento][lenParametros][1])):
                            temp = Instrucciones[elemento][lenParametros][1][i].split(" ")
                            listaValores = []
                            func = ""
                            contador = 0
                            for j in temp:
                                if isinstance(Instrucciones[elemento][lenParametros][0],list):
                                    for var in list(Instrucciones[elemento][lenParametros])[0]:
                                        pos = Instrucciones[elemento][lenParametros][0].index(var)
                                        variables[var] = Instrucciones[elemento][lenParametros][2][pos]
                                else:
                                    var = Instrucciones[elemento][lenParametros][0]
                                    pos = Instrucciones[elemento][lenParametros][0].index(var)
                                    variables[var] = Instrucciones[elemento][lenParametros][2][pos]
                                if j in Instrucciones[elemento][lenParametros][0] and (
                                        temp[contador - 1] != "Inic" or j != temp[contador]) and ("[Inc" not in temp and "Inc" not in temp and "[Inic" not in temp):
                                    pos = Instrucciones[elemento][lenParametros][0].index(j)
                                    valor = Instrucciones[elemento][lenParametros][2][pos]
                                    listaValores.append(str(valor))
                                elif j == (str(Instrucciones[elemento][lenParametros][0]) + "," ) and (temp[contador - 1] != "Inic" or j != temp[contador]) \
                                        and ("[Inc" not in temp and "Inc" not in temp and "[Inic" not in temp):
                                    j = j[0:-1]
                                    pos = Instrucciones[elemento][lenParametros][0].index(j)
                                    valor = str(Instrucciones[elemento][lenParametros][2][pos]) + ","
                                    listaValores.append(str(valor))
                                elif j == str(Instrucciones[elemento][lenParametros][0]) + "]" and (
                                        temp[contador - 1] != "Inic" or j != temp[contador]) and ("[Inc" not in temp and "Inc" not in temp and "[Inic" not in temp):
                                    j = j[0:-1]
                                    pos = Instrucciones[elemento][lenParametros][0].index(j)
                                    valor = str(Instrucciones[elemento][lenParametros][2][pos]) + "]"
                                    listaValores.append(str(valor))
                                elif j in Instrucciones[elemento][lenParametros][0] and (temp[contador - 1] == "Inic"):
                                    flag = True
                                    if isinstance(Instrucciones[elemento][lenParametros][0],str):
                                        flag = False
                                        if j == Instrucciones[elemento][lenParametros][0]:
                                            flag = True
                                    if temp.index("Inic") + 1 != contador and flag:
                                        pos = Instrucciones[elemento][lenParametros][0].index(j)
                                        valor = Instrucciones[elemento][lenParametros][2][pos]
                                        listaValores.append(str(valor))
                                    else:
                                        listaValores.append(j)
                                elif j in Instrucciones[elemento][lenParametros][0] and (temp[0] == "[Inic"):
                                    flag = True
                                    if isinstance(Instrucciones[elemento][lenParametros][0], str):
                                        flag = False
                                        if j == Instrucciones[elemento][lenParametros][0]:
                                            flag = True
                                    if temp.index("[Inic") + 1 != contador and flag:
                                        pos = Instrucciones[elemento][lenParametros][0].index(j)
                                        valor = Instrucciones[elemento][lenParametros][2][pos]
                                        listaValores.append(str(valor))
                                    else:
                                        listaValores.append(j)
                                else:
                                    listaValores.append(j)
                                contador += 1
                            cont = 0
                            for g in listaValores:
                                if cont == 0:
                                    func += g
                                else:
                                    func += " " + g
                                cont += 1
                            if "Inic" not in func:
                                listaFinal.append(func)
                            else:
                                for i in duplicatedIndex(temp,"Inic"):
                                    if key_exists(variables,temp[i+1]) and Instrucciones[elemento][lenParametros][pos] == temp[i+1]:
                                        parser.parse(func)
                                        Instrucciones[elemento][lenParametros][2][pos] = variables[temp[i+1]]
                                        listaFinal.append(func)
                                    else:
                                        listaFinal.append(func)
                        for inst in listaFinal:
                            if "Repite" not in Entrada and isinstance(Entrada, str):
                                EntradaTemp = Entrada
                                Entrada = str(inst)
                                parser.parse(inst)
                                Entrada = EntradaTemp
                                print(inst)
                                listaEjecuta.append(toDo)
                            elif 'Inic' in inst:
                                Entrada = str(inst)
                                parser.parse(inst)
                                print(inst)
                                listaEjecuta.append(toDo)
                        toDo = listaEjecuta


def p_Ejecuta_Funcion(p):
    """
    function :  Ejecuta Space NAME
    """
    global Error, toDo, listaEjecuta, Entrada, Funcion
    nombre = p[3]
    InicioEjecuta = p[1] + ' ' + nombre
    Ejecutar = True
    if InicioEjecuta == Entrada[:len(InicioEjecuta)]:
        Ejecutar = False
    if nombre not in Instrucciones and Ejecutar:
        Error = str("No existe la funcion de nombre " + nombre)
    elif not Funcion:
        for elemento in Instrucciones:
            if elemento == nombre:
                if key_exists(Instrucciones[elemento], 0):
                    for instruccion in Instrucciones[elemento][0][1]:
                        if "Repite" not in Entrada and isinstance(Entrada, str):
                            EntradaTemp = Entrada
                            Entrada = str(instruccion)
                            parser.parse(instruccion)
                            listaEjecuta.append(toDo)
                            Entrada = EntradaTemp
                    toDo = listaEjecuta

# Función que ejecuta las órdenes
def p_Ejecuta_Ordenes(p):
    """
    function : Ejecuta Space LeftSquareBracket funciones RightSquareBracket
             | Ejecuta Space LeftSquareBracket statement RightSquareBracket
    """
    global listaEjecuta, toDo, Repite,Entrada, can_Repites
    Repite = False
    lista=[]
    InicioEjecuta = p[1]
    Ejecutar = True
    if InicioEjecuta != Entrada[:len(InicioEjecuta)]:
        Ejecutar = False
    if isinstance(Entrada, str) and Ejecutar:
        if "[" in Entrada:
            while Entrada[0] != "[":
                Entrada = Entrada[1:]
            Entrada = Entrada[1:-1]
        lista = Entrada.split(",")
    n=0
    while n < len(lista) and Ejecutar:
        if('[' in lista[n] and ']' not in lista[n]):
            cant=n+1
            ant=lista[:n]
            asig=lista[n]
            while (']' not in lista [cant]):
                asig+=','+lista[cant]
                cant+=1
            asig+= ','+lista[cant]
            if(len(lista)==cant+1):
                lista = ant + [asig]
                n=len(lista)-1
            else:
                lista=ant+[asig]+lista[cant+1:]
                n=len(ant+[asig])
        if n>0:
            lista[n]= lista[n][1:]
            n+=1
        else:
            n+=1
    if Ejecutar:
        for x in lista:
            if x[0]== ' ':
                x= x[1:]
            Entrada = x
            can_Repites=0
            parser.parse(x)
            if not(Funcion):
                listaEjecuta.append(toDo)
            toDo=""
    if not Funcion and Ejecutar:
        toDo = listaEjecuta


# Reinicia el compilador
def reiniciar():
    global Entrada, Funcion, toDo, Error, listaEjecuta, Comentario, variables, Instrucciones, ListaFunciones, Repite, can_Repites
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
    can_Repites = 0


# Funcion que devuelve True si la dos numeros son iguales
def iguales(tupla):
    global toDo
    if (tupla[0] == tupla[1]):
        toDo = "printConsola(string = 'Verdadero')"
        return "CIERTO"
    else:
        toDo = "printConsola(string = 'Falso')"
        return "FALSO"


def p_iguales(p):
    """
    function : Iguales Space operaciones
    """
    a = iguales(p[3])
    p[0] = (p[1], a, p[3])


# Funcion que devuelve CIERTO si dos condiciones se cumplen
def y(tupla):
    if (tupla[0] == "CIERTO" and tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"


def p_Y(p):
    """
    function : Y Space function Space function
    """
    res = y((p[3][1], p[5][1]))
    p[0] = (p[1], res, p[3], p[5])
    print(p[0])


# Funcion que devuelve CIERTO si al menos una condicion se cumple
def O(tupla):
    if (tupla[0] == "CIERTO" or tupla[1] == "CIERTO"):
        return "CIERTO"
    else:
        return "FALSO"


def p_O(p):
    """
    function : O Space function Space function
    """
    a = O((p[3][1], p[5][1]))
    p[0] = (p[1], a, p[3], p[5])


# Funcion que devuelve CIERTO si n > n1
def MayorQue(num1, num2):
    global toDo
    if (num1 > num2):
        toDo = "printConsola(string = 'Verdadero')"
        return "CIERTO"
    else:
        toDo = "printConsola(string = 'Falso')"
        return "FALSO"


def p_MayorQue(p):
    """
    function : MayorQue Space expression PuntoComa Space expression
    """
    a = MayorQue(p[3][1], p[6][1])
    p[0] = (p[1], a, p[3])


# Funcion que devuelve Falso si n < n1
def MenorQue(num1, num2):
    global toDo
    if (num1 < num2):
        toDo = "printConsola(string = 'Verdadero')"
        return "CIERTO"
    else:
        toDo = "printConsola(string = 'Falso')"
        return "FALSO"


def p_MenorQue(p):
    """
    function : MenorQue Space expression PuntoComa Space expression
    """
    a = MenorQue(p[3][1], p[6][1])
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


# Funcion para restar los digitos de una tupla
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
    global Entrada, listaEjecuta, toDo, Repite, can_Repites
    flagrepite = False
    can_Repites += 1
    Inicial=Entrada
    if isinstance(Entrada, str):
        if "[" in Entrada:
            while Entrada[0] != "[":
                Entrada = Entrada[1:]
            Entrada = Entrada[1:-1]
        Entrada = Entrada.split(",")
    n=0
    while n < len(Entrada):
        if('[' in Entrada[n] and ']' not in Entrada[n]):
            cant=n+1
            ant=Entrada[:n]
            asig=Entrada[n]
            while (']' not in Entrada [cant]):
                asig+=','+Entrada[cant]
                cant+=1
            asig+= ','+Entrada[cant]
            if(len(Entrada)==cant+1):
                Entrada = ant + [asig]
                n=len(Entrada)-1
            else:
                Entrada=ant+[asig]+Entrada[cant+1:]
                n=len(ant+[asig])
        if n>0:
            Entrada[n]= Entrada[n][1:]
            n+=1
        else:
            n+=1
    canRepite = 0
    for elemento in Entrada:
        if "Repite" in elemento:
            canRepite += 1
    if canRepite == can_Repites - 1:
        flagrepite = True
    a = Entrada
    while can_veces != 0 and flagrepite:
        s = Entrada[0]
        if s[0]== ' ':
            s= s[1:]
        Entrada = s
        guardar = can_Repites
        can_Repites = 0
        parser.parse(s)
        can_Repites = guardar
        Entrada = a
        listaEjecuta.append(toDo)
        num = 1
        while len(Entrada) != num:
            s = Entrada[num]
            if s[0] == ' ':
                s = s[1:]
            print(s)
            Entrada = s
            num += 1
            guardar = can_Repites
            can_Repites = 0
            parser.parse(s)
            can_Repites = guardar
            Entrada = a
            listaEjecuta.append(toDo)
        toDo = listaEjecuta
        can_veces -= 1
        can_Repites = 0
    Entrada= Inicial


# Ejecuta si se cumple la condicion
def p_Si(p):
    """
    function : Si Space  expression LeftSquareBracket function RightSquareBracket
             | Si Space expression LeftSquareBracket funciones RightSquareBracket
    """
    global toDo
    p[0] = (p[1], p[3], p[5])
    if (p[0][1][1] == 'CIERTO'):
        print("EJECUTA")
        repite((1, None))
    else:
        print("NO EJECUTA")
        toDo = ""


# Funcion que repite ordenes N cantidad de veces
def p_Repite(p):
    """
    function : Repite Space expression Space LeftSquareBracket funciones RightSquareBracket
             | Repite Space expression Space LeftSquareBracket statement RightSquareBracket
    """
    global Repite, Funcion
    p[0] = (p[3][1], p[5])
    Repite = False
    if Funcion == False:
        repite(p[0])


# Acepta nombres de variables
def p_Variable(p):
    """
    Variable : NAME Coma Space NAME
             | NAME Coma Space Variable
    """
    p[0] = (p[1], p[4])


# Acepta nombres y funciones para variables
def p_Variables(p):
    """
    Variables : expression
              | expression Coma Space Variables
    """
    if len(p) > 2:
        p[0] = (p[1], p[4])
    else:
        p[0] = (p[1])


# Detecta el fin de una funcion
def p_Fin(p):
    """
    function : Fin
    """
    global Funcion, Error
    if Funcion:
        Funcion = False
        print(Instrucciones)
    else:
        Error = 'No existe un Para'


# Gramatica para creacion de una funcion sin variables
def p_ParaSin(p):
    """
    function : Para Space NAME Space LeftSquareBracket RightSquareBracket
    """
    global Funcion, Error, lenPar
    lenPar = 0
    if Funcion == True:
        Error = "Error no puede crear un 'Para' dentro de otro"
    else:
        Funcion = True
        if p[3] not in Instrucciones or (not key_exists(Instrucciones[p[3]], 0)):
            if p[3] not in Instrucciones:
                Instrucciones[p[3]] = {0: [[None], []]}
            else:
                Instrucciones[p[3]][0] = {[[None], []]}
            print(Instrucciones)
        else:
            Error = str("La funcion con nombre '%s' ya fue creada" % p[3])


# Gramatica para la creacion de una funcion con variables
def p_ParaVarias(p):
    """
    function : Para Space NAME Space LeftSquareBracket Variable RightSquareBracket
    """
    global Funcion, Error, Instrucciones, lenPar
    variable = makeList(p[6])
    cantidadVariables = len(variable)
    lenPar = cantidadVariables
    if Funcion == True:
        Error = "Error no puede meter un Para dentro de otro"
    else:
        Funcion = True
        for var in variable:
            parser.parse("Var " + str(var))
        if p[3] not in Instrucciones or (not key_exists(Instrucciones[p[3]], cantidadVariables)):
            var = makeList(p[6])
            if p[3] not in Instrucciones:
                Instrucciones[p[3]] = {cantidadVariables: [var, [], []]}
            else:
                Instrucciones[p[3]][cantidadVariables] = [var, [], []]
        else:
            Error = str("La funcion con nombre '%s' y esa cantidad de parametros ya fue creada" % p[3])
    print("Inst " + str(Instrucciones))


# Gramatica para la creacion de una funcion con una variable
def p_ParaUna(p):
    """
    function : Para Space NAME Space LeftSquareBracket NAME RightSquareBracket
    """
    global Funcion, Error, Instrucciones, lenPar
    lenPar = 1
    variable = "Var " + p[6]
    if Funcion == True:
        Error = str("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True
        parser.parse(variable)
        if p[3] not in Instrucciones or (not key_exists(Instrucciones[p[3]], 1)):
            if p[3] not in Instrucciones:
                Instrucciones[p[3]] = {1: [p[6], [], []]}
            else:
                Instrucciones[p[3]][1] = [p[6], [], []]
        else:
            Error = str("La funcion con nombre '%s' ya fue creada" % p[3])


# Retorna error de sintaxis
def p_error(p):
    global Error, Entrada
    if p:
        Error = str("Error de sintaxis en '%s'" % p.value)
    else:
        if lexError:
            Error=lexError
        else:
            Error = str("Error de sintaxis")


parser = yacc.yacc()
# while not Error:
#     global Entrada
#     s = input('->')
#     Entrada = s
#     if not s:
#         continue
#     # try:
#     parser.parse(s)
#     Repite = True
#     # except Exception as e:
#     #     if not Error:
#     #         Error = str(e)
print(Error)

# Hacer la documentacion
# Errores del dia
# Arreglar el si
# Arreglar repite en para
