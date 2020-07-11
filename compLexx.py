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
    'RightSquareBracket'
]
#indica con que simbolo se representan los tokens
t_EQUALS = r'\='
t_LeftSquareBracket = r'\['
t_RightSquareBracket = r'\]'

#Comentarios
def t_Comment(t):
    r'\//[a-zA-Z_0-9]*'
    pass

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
    r'Borrarpantalla'
    t.type = 'Borrarpantalla'
    return t


#Error al ingresar un caracter no permitido
def t_error(t):
    print("Caracter no aceptado '%s' " % t.value[0] )
    t.lexer.skip(1)

lexer = lex.lex()

