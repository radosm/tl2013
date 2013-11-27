import ply.lex as lex

tokens = ('UINT', 'FLOAT', 'PLAY', 'SIN', 'SIL', 'EXPAND', 'REDUCE')
literals = '{}().;,&+-*/'
t_PLAY = r'play'
t_SIN = r'sin'
t_SIL = r'silence|sil'
t_EXPAND = r'expand'
t_REDUCE = r'reduce'

def t_FLOAT(t):
    r'-?\d*\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t

def t_UINT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t

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
