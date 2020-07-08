import ply.lex as lex

import sys

#lista de variables que son aceptadas
tokens = [
    'NAME',
    'EQUALS',
    'FLOAT',
    'INT'
]
#indica con que simbolo se representan los tokens
t_EQUALS = r'\='

#Comentarios
def t_Comment(t):
    r'\//[a-zA-Z_0-9]*'
    pass

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

#Error al ingresar un caracter no permitido
def t_error(t):
    print("Caracter no aceptado '%s' " % t.value[0] )
    t.lexer.skip(1)

lexer = lex.lex()

