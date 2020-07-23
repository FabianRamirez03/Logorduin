import ply.lex as lex
import sys

#lista de variables que son aceptadas
tokens = [
    'NAME',
    'EQUALS',
    'FLOAT',
    'INT',
    'Azar',
    'Menos',
    'Producto',
    'Potencia',
    'Division',
    'Resto',
    'RC',
    'Sen',
    'Suma',
    'Elegir',
    'Cuenta',
    'Ultimo',
    'Elemento',
    'Pri',
    'Borrapantalla',
    'Space',
    'LeftSquareBracket',
    'RightSquareBracket',
    'Var',
    'Inic',
    'Inc',
    'PonCL',
    'PonColorLapiz',
    'Centro',
    'Espera',
    'Ejecuta',
    'Repite',
    'Si',
    'Iguales',
    'Y',
    'O',
    'MayorQue',
    'MenorQue',
    'Redondea',
    'Cos',
    'Diferencia',
    'Avanza',
    'Retrocede',
    'GiraDerecha',
    'GiraIzquierda',
    'OcultaTortuga',
    'ApareceTortuga',
    'PonXY',
    'PonRumbo',
    'Rumbo',
    'PonX',
    'PonY',
    'BajaLapiz',
    'SubeLapiz',
    'Coma',
    'PuntoComa',
    'Para',
    'Fin',
    'Comentario'
]
#indica con que simbolo se representan los tokens
t_EQUALS = r'\='
t_LeftSquareBracket = r'\['
t_RightSquareBracket = r'\]'
t_Coma = r','
t_PuntoComa = r';'

#Comentarios
def t_Comentario(t):
    r'\//[ \t\na-zA-Z_0-9&@-]*'
    t.value ='Comentario'
    return t

#espacio
def t_Space(t):
    r'[ \t\n]+'
    return t

#define float como uno o mas numeros seguido de  '.' seguido de otros numeros
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

#define int como una sucesion de numeros
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

#define las reglas de inicializacion de las variables
def t_NAME(t):
    r'[a-z][a-zA-Z_0-9&@-]*'
    t.type = 'NAME'
    return t

def t_var(t):
    r'Var'
    t.type = 'Var'
    return t

def t_Para(t):
    r'Para'
    t.type = 'Para'
    return t

def t_Fin(t):
    r'Fin'
    t.type = 'Fin'
    return t

def t_Avanza(t):
    r'Avanza'
    t.type = 'Avanza'
    return t

def t_Retrocede(t):
    r'Retrocede'
    t.type = 'Retrocede'
    return t

def t_GiraDerecha(t):
    r'GiraDerecha'
    t.type = 'GiraDerecha'
    return t

def t_GiraIzquierda(t):
    r'GiraIzquierda'
    t.type = 'GiraIzquierda'
    return t

def t_OcultaTortuga(t):
    r'OcultaTortuga'
    t.type = 'OcultaTortuga'
    return t

def t_ApareceTortuga(t):
    r'ApareceTortuga'
    t.type = 'ApareceTortuga'
    return t

def t_PonXY(t):
    r'PonXY'
    t.type = 'PonXY'
    return t

def t_PonRumbo(t):
    r'PonRumbo'
    t.type = 'PonRumbo'
    return t

def t_Rumbo(t):
    r'Rumbo'
    t.type = 'Rumbo'
    return t

def t_PonX(t):
    r'PonX'
    t.type = 'PonX'
    return t

def t_PonY(t):
    r'PonY'
    t.type = 'PonY'
    return t

def t_BajaLapiz(t):
    r'BajaLapiz'
    t.type = 'BajaLapiz'
    return t

def t_SubeLapiz(t):
    r'SubeLapiz'
    t.type = 'SubeLapiz'
    return t

def t_Inc(t):
    r'Inc'
    t.type = 'Inc'
    return t

def t_Inic(t):
    r'Inic'
    t.type = 'Inic'
    return t

def t_Suma(t):
    r'Suma'
    t.type = 'Suma'
    return t

#definicion de funciones del nuevo lenguaje
def t_Azar(t):
    r'Azar'
    t.type = 'Azar'
    return t

def t_Menos(t):
    r'Menos'
    t.type = 'Menos'
    return t

def t_Producto(t):
    r'Producto'
    t.type = 'Producto'
    return t

def t_Potencia(t):
    r'Potencia'
    t.type = 'Potencia'
    return t

def t_Division(t):
    r'Division'
    t.type = 'Division'
    return t

def t_Resto(t):
    r'Resto'
    t.type = 'Resto'
    return t

def t_RC(t):
    r'RC'
    t.type = 'RC'
    return t

def t_Sen(t):
    r'Sen'
    t.type = 'Sen'
    return t

def t_Elegir(t):
    r'Elegir'
    t.type = 'Elegir'
    return t

def t_Cuenta(t):
    r'Cuenta'
    t.type = 'Cuenta'
    return t

def t_Ultimo(t):
    r'Ultimo'
    t.type = 'Ultimo'
    return t

def t_Elemento(t):
    r'Elemento'
    t.type = 'Elemento'
    return t

def t_Pri(t):
    r'Pri'
    t.type = 'Pri'
    return t

def t_Borrarpantalla(t):
    r'Borrapantalla'
    t.type = 'Borrapantalla'
    return t
def t_PonColor(t):
    r'PonColorLapiz'
    t.type = 'PonColorLapiz'
    return t
def t_PonCl(t):
    r'PonCL'
    t.type = 'PonCL'
    return t
def t_Centro(t):
    r'Centro'
    t.type = 'Centro'
    return t
def t_Espera(t):
    r'Espera'
    t.type = 'Espera'
    return t
def t_Ejecuta(t):
    r'Ejecuta'
    t.type = 'Ejecuta'
    return t
def t_Repite(t):
    r'Repite'
    t.type = 'Repite'
    return t
def t_Si(t):
    r'Si'
    t.type = 'Si'
    return t
def t_Iguales(t):
    r'Iguales'
    t.type = 'Iguales'
    return t
def t_Y(t):
    r'Y'
    t.type = 'Y'
    return t
def t_O(t):
    r'O'
    t.type = 'O'
    return t
def t_MayorQue(t):
    r'MayorQue'
    t.type = 'MayorQue'
    return t
def t_MenorQue(t):
    r'MenorQue'
    t.type = 'MenorQue'
    return t
def t_Redondea(t):
    r'Redondea'
    t.type = 'Redondea'
    return t
def t_Cos(t):
    r'Cos'
    t.type = 'Cos'
    return t
def t_Diferencia(t):
    r'Diferencia'
    t.type = 'Diferencia'
    return t

#Error al ingresar un caracter no permitido
def t_error(t):
    print("Caracter no aceptado '%s' " % t.value[0] )
    t.lexer.skip(1)

lexer = lex.lex()

