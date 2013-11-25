import ply.lex as lex
import re

#tokens = ('INT', 'PARFLOAT', 'CONCAT', 'DOT', 'PLAY')
literals = '{}'
t_CONCAT = r';'
t_DOT = r'\.'
t_PLAY = r'play'

def t_INT(t):
    r'[-+]?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t

def t_FLOAT(t):
    r'[-+]?\d*\.?\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t

'''
def t_PARFLOAT(t):
    r'\([-+]?\d*\.?\d+\)'
    try:
        t.value = float(re.match('\(([-+]?\d*\.?\d+)\)', t.value).group(1))
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t
'''

# Ignoramos espacios y tabs
t_ignore = " \t"

# Reconocemos el salto del linea solo para incrementar el contador de linea
# pero no forma parte de nuestro tokens (porque no devolvemos nada en la funcion)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Caracter invalido: %s" % t.value[0]
    t.lexer.skip(1)

# Construimos el lexer
lex.lex()
