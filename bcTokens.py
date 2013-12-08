import ply.lex as lex

literals = '{}().,'

tokens = (
    'UINT', 'INT', 'FLOAT', # Tipos basicos
    'SIN', 'LIN', 'SIL', 'NOI', # Generadores
    'CON', 'MIX', 'SUM', 'SUB', 'MUL', 'DIV', # Operadores
    'PLAY', 'POST', 'LOOP', 'TUNE', 'FILL', 'REDUCE', 'EXPAND' # Metodos
)

t_PLAY   = r'play'
t_SIN    = r'sin'
t_SIL    = r'silence|sil'
t_NOI    = r'noise|noi'
t_LIN    = r'linear|lin'
t_EXPAND = r'expand'
t_REDUCE = r'reduce'
t_POST   = r'post'
t_LOOP   = r'loop'
t_TUNE   = r'tune'
t_FILL   = r'fill'
t_CON    = r'con|;'
t_MIX    = r'mix|&'
t_SUM    = r'sum|\+'
t_SUB    = r'sub|-'
t_MUL    = r'mul|\*'
t_DIV    = r'div|/'

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

def t_INT(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Valor invalido: %s" % t.value
        t.value = 0
    return t

# Ignoramos espacios y tabs
t_ignore = " \t"

# Ignoramos los comentarios
def t_nocomments(t):
    r'//[^\n]+'

# Reconocemos el salto del linea solo para incrementar el contador de linea pero
# no forma parte de nuestro tokens (porque no devolvemos nada en la funcion)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print "Caracter invalido: %s" % t.value[0]
    t.lexer.skip(1)

# Construimos el lexer
lexer = lex.lex()
