import config
import ply.yacc as yacc
from bcTokens import *
from numpy import *
import pygame
pygame.init()
pygame.mixer.init(frequency=config.SAMPLING_RATE, size=config.SAMPLE_SIZE, channels=1, buffer=4096)
SONG_END = pygame.USEREVENT + 1
from debug import log

# Reglas de parsing

precedence = (
    ('left', 'CON'),
    ('left', 'MIX'),
    ('left', 'SUM', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS'), # UMINUS = Unary Minus
    ('left', '.')
)

# Diccionario de nombres
names = {}

beat=config.SAMPLING_RATE/12

def seno(c, a):
    print beat
    buff = array(range(0, beat))
    x = (c*2*pi)/beat
    for i in range(0, beat):
        buff[i] = a*sin(i*x)
    return buff

def resample(b, l):
    nuevo = array(range(0, l))
    lenB = len(b)
    for i in range(0, l):
        nuevo[i] = b[i*lenB/l]
    return nuevo

def resize(b, l):
    nuevo = array(range(0, l))
    lenB = len(b)
    for i in range(0, l):
        nuevo[i] = b[i % lenB]
    return nuevo

def fill(b, n):
    l = config.BEAT * n
    nuevo = array(range(0, l))
    for i in range(0, l):
        if i < len(b):
            nuevo[i] = b[i]
        else:
            nuevo[i] = 0.0
    return nuevo

def oper(op, buffer_a, buffer_b):
    if len(buffer_a) < len(buffer_b):
        a = resize(buffer_a, len(buffer_b))
        b = buffer_b
    else:
        a = buffer_a
        b = resize(buffer_b, len(buffer_a))
    nuevo = array(range(0, len(a)))
    for i in range(0, len(a)):
        nuevo[i] = op(a[i], b[i])
    return nuevo

def p_buffer_llaves(b):
    '''buffer : '{' buffer '}' '''
    b[0] = b[2]

def p_buffer_concat(b):
    '''buffer : buffer CON buffer'''
    b[0] = hstack((b[1], b[3]))
    log('p_buffer_concat %s;%s = %s' % (b[1], b[3], b[0]))

def p_buffer_mezcla(b):
    '''buffer : buffer MIX buffer'''
    b[0] = oper(lambda x, y: (x + y) / 2, b[1], b[3])
    log('p_buffer_mezcla: %s & %s = %s' % (b[1], b[3], b[0]))

def p_buffer_sum(b):
    '''buffer : buffer SUM buffer'''
    b[0] = oper(lambda x, y: x + y, b[1], b[3])
    log('p_buffer_sum: %s + %s = %s' % (b[1], b[3], b[0]))

def p_buffer_res(b):
    '''buffer : buffer SUB buffer'''
    b[0] = oper(lambda x, y: x - y, b[1], b[3])
    log('p_buffer_res: %s - %s = %s' % (b[1], b[3], b[0]))

def p_buffer_mul(b):
    '''buffer : buffer MUL buffer'''
    b[0] = oper(lambda x, y: x * y, b[1], b[3])
    log('p_buffer_mul: %s * %s = %s' % (b[1], b[3], b[0]))

def p_buffer_div(b):
    '''buffer : buffer DIV buffer'''
    b[0] = oper(lambda x, y: x / y, b[1], b[3])
    log('p_buffer_div: %s / %s = %s' % (b[1], b[3], b[0]))

def p_buffer_signed_int(b):
    '''buffer : '-' UINT %prec UMINUS '''
    b[0] = -b[2]
    log('p_buffer_uint: -%s = %s' % (b[2], b[0]))

def p_buffer_unsigned_int(b):
    'buffer : UINT'
    b[0] = array([b[1]])
    log('p_buffer_int: %s' % b[1])

def p_buffer_m(b):
    'buffer : m'
    b[0] = b[1]
    log('p_buffer_m: %s' % b[1])

def p_buffer_g(b):
    'buffer : g'
    b[0] = b[1]
    log('p_buffer_g: %s' % b[1])

def p_m_play(m):
    '''m : buffer '.' PLAY par
         | buffer '.' PLAY'''
    m[0] = m[1]
    if len(m) == 5:
        log('p_m_play: %s (%s)' % (m[1], m[4]))
    else:
        log('p_m_play: %s' % m[1])
    sonido = pygame.mixer.Sound(m[1])
    canal  = sonido.play()
    canal.set_endevent(SONG_END)
    
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                return

def p_m_reduce_expand(m):
    '''m : buffer '.' REDUCE par
         | buffer '.' EXPAND par '''
    l = config.BEAT * int(m[4])
    if ((m[3] == 'reduce') and (l < len(m[1]))) or \
       ((m[3] == 'expand') and (l > len(m[1]))):
        m[0] = resample(m[1], l)
    else:
        m[0] = m[1]
    log('p_m_%s: resample(%s, %s) = %s' % (m[3], m[1], l, m[0]))

def p_g(g):
    '''g : SIN par
         | SIN par2
         | LIN par2
         | NOI par
         | NOI
         | SIL'''
    ##g[0] = array([333]) if g[1][:3] == 'sil' else array([888]) # reemplazar por sin (par1, par2)
    print "**sin "+str(g[2][0]) +" "+str(g[2][1])
    g[0] = seno (g[2][0] , g[2][1])
    log('p_g: %s' % g[0])

def p_par(p):
    '''par : '(' UINT ')'
           | '(' FLOAT ')' '''
    p[0] = p[2]
    log('p_par %s' % p[2])

def p_par2(p):
    '''par2 : '(' FLOAT ',' FLOAT ')' '''
    p[0] = array([p[2],p[4]])
    log('p_par2 (%s, %s)' % (p[2], p[4]))

def p_m_post(m):
    ''' m : buffer '.' POST'''
    m[0] = m[1]
    print m[1]
    log('p_m_post: %s' % m[1])

def p_m_loop(m):
    '''m : buffer '.' LOOP par'''
    l = int(m[4])
    m[0] = tile(m[1], l)
    log('p_m_loop: %s %s' %(m[1], m[4]))

def p_m_tune(m):
    '''m : buffer '.' TUNE par'''
    p = int(m[4])
    l = int(len(m[1]) * ((2**(1.0/12))**-p))
    m[0] = resample(m[1], l)
    log('p_m_tune: %s %s' % (m[1], m[4]))

def p_m_fill(m):
    '''m : buffer '.' FILL par'''
    m[0] = fill(m[1], int(m[4]))
    log('p_m_fill: %s %s' % (m[1], m[4]))
    

def p_error(t):
    log("Error de sintaxis en: '%s'" % t.value)

yacc.yacc()
