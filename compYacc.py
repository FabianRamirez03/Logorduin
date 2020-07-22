import time

import ply.yacc as yacc
import random
import math as m
from compLexx import tokens
import sys
global Entrada,Funcion,Ejecutar
Funcion = False
coloresPermitidos = ["blanco","azul","marron","cian","gris","amarillo","negro","rojo","verde"]
ListaFunciones = {}
Instrucciones={}
variables = {}

#Gramatica de asignacion de variables
def p_statement_create(p):
    """
    statement : Var Space NAME Space EQUALS Space expression
    """

    if p[3] not in variables:
        p[0] =(p[1], p[7][1], p[3] )
        variables[p[3]] = p[7][1]
        print(p[0])
        print(variables)
    else:
        print("La variable '%s' ya fue creada" % p[3])

#Gramatica de variable vacia
def p_statement_create_empty(p):
    """
    statement : Var Space NAME
    """

    global Funcion, Entrada
    if p[3] not in variables:
        p[0] = (p[1], 0, p[3])
        variables[p[3]] = 0
        print(variables)
    else:
        print("La variable '%s' ya fue creada" % p[3])



#Inicializacion de una variable
def p_statement_assign(p):
    """
    function : Inic Space NAME Space EQUALS Space expression
             | Inic Space NAME Space EQUALS Space function
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        if p[3] not in variables:
            print("La variable '%s' no ha sido creada" % p[3])
        else:
            variables[p[3]] = p[7][1]
            p[0] = (p[1], p[7][1], p[3],p[7])


# Gramatica de una expresion
def p_statement_expr(p):
    """
    statement : expression
    """
    p[0] = p[1]
    if p[0] == None:
        return
    else:
        print(p[1][1])

def p_expression_Number(p):
    """
    expression : INT
               | FLOAT
    """
    p[0] = ('exp',p[1])

def p_expression_Function(p):
    """
    expression : function
    """
    p[0] = p[1]

def p_expression_name(p):
    """
    expression : NAME
    """
    try:
        p[0] = ('exp',variables[p[1]])
    except LookupError:# arreglaaaaaaaaaaaaaaar********************************************
        print("Variable no definida '%s'" % p[1])
        raise Exception()

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
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
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
    """
    function : Suma Space operaciones
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        a = suma(p[3])
        p[0] = (p[1],a,p[3])

def p_Incrementar(p):
    """
    function : Inc Space NAME
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        try:
            variables[p[3]] = variables[p[3]] + 1
            p[0] = (p[1], p[3],variables[p[3]])
        except LookupError:
                print("La variable que desea incrementar no ha sido declarada")

def p_Incrementar_Num(p):
    """
    function : Inc Space NAME Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        variables[p[3]] = variables[p[3]] * p[5][1] #preguntar al profe
        p[0] = (p[1], variables[p[3]], p[3],p[5][1])

# funcion de numero aleatorio
def p_Azar(p):
    """
    function : Azar Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        num = random.randint(0,p[3][1])
        p[0]= (p[1],num,p[3][1])

# funcion para cambiar de signo
def p_Menos(p):
    """
    function :  Menos Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
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
    """
    function : Producto Space operaciones
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        print(p[3])
        p[0]=(p[1],producto(p[3]),p[3][1])

# funcion para calcular potencia y gramatica
def p_Potencia(p):
    """
    function :  Potencia Space expression Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        num = p[3][1]**p[5][1]
        p[0]=(p[1],num,p[3][1],p[5][1])

def p_Division(p):
    """
    function :  Division Space expression Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        num = p[3][1]
        denom = p[5][1]
        if denom == 0:
            print("Error, no se puede dividir entre cero")
        else:
            resultado = num / denom
            p[0]=(p[1],resultado,num,denom)

def p_Resto(p):
    """
    function :  Resto Space expression Space expression
    """
    num = p[3][1]%p[5][1]
    p[0]=(p[1],num,p[3][1],p[5][1])

def p_RC(p):
    """
    function :  RC Space expression
    """
    num = m.sqrt(p[3][1])
    p[0]=(p[1],num,p[3][1])

def p_Sen(p):
    """
    function :  Sen Space expression
    """
    num = m.sin(m.radians(p[3][1]))
    p[0]=(p[1],num,p[3][1])

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
    Lista= makeList(p[6])
    p[0]=(p[1],Lista[p[3][1]-1],Lista,p[3]) #(nombre,resultado,lista,indice)

def p_Primero(p):
    """
    function : Pri Space LeftSquareBracket operaciones RightSquareBracket
    """
    Lista= makeList(p[4])
    p[0]=(p[1],Lista[0],Lista)

#BORRAR ESTO ALGUN DIA************************************************************************************
def p_Prueba(p):
    """
    function : Prueba
    """
    for elemento in Instrucciones:
        ultimoElemento=elemento
    Instrucciones[ultimoElemento][1]+=['avanza']
    Instrucciones[ultimoElemento][1]+=['casa']

def p_Avanza(p):
    """
    function : Avanza Space expression
             | Avanza Space function
    """
    global Funcion,Entrada
    if(Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Avanza '%d' unidades" % p[0][1])

def p_Retrocede(p):
    """
    function : Retrocede Space expression
             | Retrocede Space function
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Retrocede '%d' unidades" %p[0][1])

def p_GiraDerecha(p):
    """
    function : GiraDerecha Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Gira '%d' grados a la derecha" %p[0][1])

def p_GiraIzquierda(p):
    """
    function : GiraIzquierda Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Gira '%d' grados a la izquierda" %p[0][1])

def p_OcultaTortuga(p):
    """
    function : OcultaTortuga
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)
        print("Se oculta la tortuga")

def p_ApareceTortuga(p):
    """
    function : ApareceTortuga
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)
        print("Aparece la Tortuga")

def p_PonXY(p):
    """
    function : PonXY Space LeftSquareBracket expression Space expression RightSquareBracket
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        a = [p[4][1],p[6][1]]
        p[0] = (p[1],a,p[4][1],p[6][1])

def p_PonRumbo(p):
    """
    function : PonRumbo Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1], p[3][1])
        print("Tortuga en rumbo hacia los '%d' grados" %p[0][1])

def p_Rumbo(p):
    """
    function : Rumbo
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)
        print("Indicar el rumbo de la tortura")

def p_PonX(p):
    """
    function : PonX Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],p[3][1])
        print("Tortuga en la posicionX '%d'"%p[0][1])

def p_PonY(p):
    """
    function : PonY Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],p[3][1])
        print("Tortuga en la posicionY '%d'" % p[0][1])

def p_BajaLapiz(p):
    """
    function : BajaLapiz
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)
        print("Comienza a dibujar")

def p_SubeLapiz(p):
    """
    function : SubeLapiz
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)
        print("Levanta el lapiz y detiene el dibujo")

def p_Borrapantalla(p):
    """function : Borrapantalla"""
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)

# Funcion para cambiar el color del lapiz
def p_Poncolorlapiz(p):
    """
    function :  PonColorLapiz Space NAME
    """
    global Funcion, Entrada
    color = p[3]
    if color not in coloresPermitidos:
        print("Error, el color " + color + " no es un color permitido")
    else:
        if (Funcion):
            for elemento in Instrucciones:
                ultimoElemento = elemento
            Instrucciones[ultimoElemento][1] += [Entrada]
        else:
            p[0] = (p[1],p[3])

# Funcion para poner la tortuga en el centro
def p_Centro(p):
    """
    function :  Centro
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        p[0] = (p[1],None)

# Funcion para pausar la ejecucion
def p_Espera(p):
    """
    function :  Espera Space expression
    """
    global Funcion, Entrada
    if (Funcion):
        for elemento in Instrucciones:
            ultimoElemento = elemento
        Instrucciones[ultimoElemento][1] += [Entrada]
    else:
        time.sleep(p[3][1]/60)
        p[0] = (p[1],p[3][1])
        print("Wait de " + str(p[3][1]/60) + " segundos")

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
    parametros = Var_Array(makeList(p[6]))
    nombre = p[3]
    if nombre not in Instrucciones:
        print("No existe la funcion de nombre " + nombre)
    else:
        for elemento in Instrucciones:
            if elemento == nombre:
                if len(parametros) != len(Instrucciones[elemento][0]):
                    print("La cantidad de parametros ingresados no coincide con la cantidad de variables de la funcion")
                else:
                    Instrucciones[elemento][2] = parametros
            listaFinal =[]
            for i in range(0,len(Instrucciones[elemento][1])):
                temp = Instrucciones[elemento][1][i].split(" ")
                listaValores = []
                func = ""

                for j in temp:
                    if j in Instrucciones[elemento][0]:
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
                listaFinal.append(func)
        for inst in listaFinal:
            parser.parse(inst)

# Funcion que ejecuta las Ordenes
def p_Ejecuta_Funcion(p):
    """
    function :  Ejecuta Space NAME
    """
    nombre = p[3]
    if nombre not in Instrucciones:
        print("No existe la funcion de nombre " + nombre)
    else:
        for elemento in Instrucciones:
            if elemento == nombre:
                for instruccion in Instrucciones[elemento][1]:
                    parser.parse(instruccion)


#Reinicia el compilador
def reiniciar():
    global variables, Instrucciones, ListaFunciones
    variables = {}
    Instrucciones = {}
    ListaFunciones = {}

# Funcion que devuelve True si la dos numeros son iguales
def iguales(tupla):
    if(tupla[0] == tupla[1]):
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
    if(tupla[0] == "CIERTO" and tupla[1] == "CIERTO"):
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
    if(tupla[0] == "CIERTO" or tupla[1] == "CIERTO"):
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
def MayorQue(num1,num2):
    if(num1 > num2):
        return "CIERTO"
    else:
        return "FALSO"

def p_MayorQue(p):
    """
    function : MayorQue Space expression PuntoComa Space expression
    """
    a= MayorQue(p[3][1],p[6][1])
    p[0] = (p[1], a, p[3])

# Funcion que devuelve Falso si n < n1
def MenorQue(num1,num2):
    if(num1 < num2):
        return "CIERTO"
    else:
        return "FALSO"

def p_MenorQue(p):
    """
    function : MenorQue Space expression PuntoComa Space expression
    """
    a= MenorQue(p[3][1],p[6][1])
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
    resta=0
    while (type(tupla[1]) == tuple):
        resta = tupla[0] - tupla[1][0]
        tupla = (resta,tupla[1][1])
    return tupla[0] - tupla[1]

def p_restar(p):
    """
    function : Diferencia Space operaciones
    """
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
    """
    function : Si Space  expression LeftSquareBracket function RightSquareBracket
             | Si Space expression LeftSquareBracket funciones RightSquareBracket
    """
    p[0] = (p[1],p[3],p[5])
    if(p[0][1][1] == 'CIERTO'):
        print("EJECUTA")
        repite((2,None))
    else:
        print("NO EJECUTA")


# Funcion que repite ordenes N cantidad de veces
def p_Repite(p):
    """
    function : Repite Space expression LeftSquareBracket funciones RightSquareBracket
             | Repite Space expression LeftSquareBracket  statement RightSquareBracket
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
    Variables : expression Coma Space expression
              | expression Coma Space Variables
    """
    p[0] = (p[1],p[4])

def p_Fin(p):
    """
    function : Fin
    """
    global Funcion
    Funcion = False
    print(Instrucciones)

def p_ParaSin(p):
    """
    function : Para Space NAME Space LeftSquareBracket RightSquareBracket
    """
    global Funcion

    if Funcion == True:
        print("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True
        if p[3] not in Instrucciones:
            Instrucciones[p[3]] = [[None],[]]
            print(Instrucciones)
        else:
            print("La funcion con nombre '%s' ya fue creada" % p[3])

def p_ParaUna(p):
    """
    function : Para Space NAME Space LeftSquareBracket NAME RightSquareBracket
    """
    global Funcion
    variable = "Var " + p[6]
    if Funcion == True:
        print("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True
        parser.parse(variable)
        if p[3] not in Instrucciones:
            Instrucciones[p[3]] = [p[6], [], []]
            print(Instrucciones)
        else:
            print("La funcion con nombre '%s' ya fue creada" % p[3])

def p_ParaVarias(p):
    """
    function : Para Space NAME Space LeftSquareBracket Variable RightSquareBracket
    """
    global Funcion
    variable = makeList(p[6])
    if Funcion == True:
        print("Error no puede meter un Para dentro de otro")
    else:
        Funcion = True

        for var in variable:
            parser.parse("Var " + str(var))

        if p[3] not in Instrucciones:
            var = makeList(p[6])
            Instrucciones[p[3]] = [var, [], []]
            print(Instrucciones)
        else:
            print("La funcion con nombre '%s' ya fue creada" % p[3])

# Retorna error de sintaxis
def p_error(p):
    if p:
        print ("Error de sintaxis de '%s'" % p.value)
        raise Exception()
    else:
        print ("Syntax error at EOF")
        raise Exception()

parser = yacc.yacc()

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
#Todo_lo que tenga parser.parse hay que agregar try except
