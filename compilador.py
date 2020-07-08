import ply.lex as lex
import ply.yacc as yacc
import sys

#Lexer
lexer = lex.lex()

# Build the parser
parser = yacc.yacc()

#lista de variables que son aceptadas
tokens = [
    'VARIABLE',
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
def t_VARIABLE(t):
    r'[a-z][a-zA-Z_0-9&@-]*'
    t.type = 'VARIABLE'
    return t

#Error al ingresar un caracter no permitido
def t_error(t):
    print("Caracter no aceptado")
    t.lexer.skip(1)


#asigna
def p_var_assign(p):
    '''
    var_assign : VARIABLE EQUALS expression
    '''
    # Build our tree
    p[0] = ('=', p[1], p[3])

#
def p_expression_var(p):
    '''
    expression : VARIABLE
    '''
    p[0] = ('var', p[1])

#Error al asignar alguna variable
def p_error(p):
    print("Syntax error found!")

#permite no asign
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None