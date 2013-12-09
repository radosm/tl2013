import config
import random
import ply.yacc as yacc
from bcTokens import *
from numpy import *
import pygame
pygame.init()
pygame.mixer.init(frequency = config.SAMPLING_RATE, size = config.SAMPLE_SIZE, channels = 1, buffer = 4096)
FIN_PLAY = pygame.USEREVENT + 1
from debug import log, errorTipos

# Reglas de parsing

precedence = (
    ('left', 'CON'),
    ('left', 'MIX'),
    ('left', 'ADD', 'SUB'),
    ('left', 'MUL', 'DIV'),
    ('left', '.')
)

# Diccionario de nombres
names = {}

def bcSin(c, a = 1.0):

    if (a<=0 or a>1):
        errorTipos('SIN: valores fuera de rango para amplitud');
    if (c<0 or c!=int(c)):
        errorTipos('SIN: valores fuera de rango para ciclos');

    buff = array(range(0, config.BEAT), dtype = float)
    x = (c * 2 * pi) / config.BEAT
    for i in range(0, config.BEAT):
        buff[i] = a * sin(i * x)
    return buff

def lin(a, b):

    if (a<-1 or a>1 or b<-1 or b>1):
        errorTipos('LIN: valores fuera de rango');

    buff = array(range(0, config.BEAT), dtype = float)
    x = float((b - a)) / (config.BEAT-1)
    for i in range(0, config.BEAT):
        buff[i] = a + x * i
    return buff

def sil():
    buff = array(range(0, config.BEAT), dtype = float)
    for i in range(0, config.BEAT):
        buff[i] = 0
    return buff

def noi(a = 1.0):

    if (a<=0 or a>1):
        errorTipos('NOI: valores fuera de rango para amplitud');

    buff = array(range(0, config.BEAT), dtype = float)
    for i in range(0, config.BEAT):
        buff[i] = a * random.uniform(-1, 1)
    return buff

def resample(b, l):

    if (l<0 or l!=int(l)):
        errorTipos('RESAMPLE: valores fuera de rango para nueva longitud');
    
    nuevo = array(range(0, l), dtype = float)
    lenB = len(b)
    for i in range(0, l):
        nuevo[i] = b[i * lenB / l]
    return nuevo

def resize(b, l):

    if (l<0 or l!=int(l)):
        errorTipos('RESIZE: valores fuera de rango para nueva longitud');
    
    nuevo = array(range(0, l), dtype = float)
    lenB = len(b)
    for i in range(0, l):
        nuevo[i] = b[i % lenB]
    return nuevo

def fill(b, n):
    l = config.BEAT * n
    nuevo = array(range(0, l), dtype = float)
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
    nuevo = array(range(0, len(a)), dtype = float)
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

def p_buffer_add(b):
    '''buffer : buffer ADD buffer'''
    b[0] = oper(lambda x, y: x + y, b[1], b[3])
    log('p_buffer_add: %s + %s = %s' % (b[1], b[3], b[0]))

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

##def p_buffer_masmenos(b):
##    '''buffer : num snum'''
##
##    if b[1]<-1 or b[1]>1 or b[2]<-1 or b[2]>1:
##        errorTipos('Valores de buffer deben estar en [-1,1]')
##
##    b[0] = array([b[1] + b[2]], dtype = float)
##    log('p_buffer_masmenos: %s %s = %s' % (b[1], b[2], b[0]))

def p_buffer_snum(b):
    '''buffer : buffer snum'''

    if b[2]<-1 or b[2]>1:
        errorTipos('Valores de buffer deben estar en [-1,1]')

    b[0] = oper(lambda x, y: x + y, b[1], array([b[2]]))
    log('p_buffer_snum: %s + %s = %s' % (b[1], b[2], b[0]))

def p_buffer_num(b):
    '''buffer : num '''

    if b[1]<-1 or b[1]>1:
        errorTipos('Valores de buffer deben estar en [-1,1]')

    b[0] = array([b[1]], dtype = float)
    log('p_buffer_num: %s' % b[1])

def p_buffer_m(b):
    'buffer : m'
    b[0] = b[1]
    log('p_buffer_m: %s' % b[1])

def p_buffer_g(b):
    'buffer : g'
    b[0] = b[1]
    log('p_buffer_g: %s' % b[1])

def fixRanges(buf):
    for i in range(0, len(buf)):
        buf[i] *= pow(2, 15)
        if buf[i] < -pow(2, 15):
            buf[i] = -pow(2, 15)
        elif buf[i] >= pow(2, 15):
            buf[i] = pow(2, 15) - 1
    return buf

def p_m_play(m):
    '''m : buffer '.' PLAY par
         | buffer '.' PLAY'''
    buf = fixRanges(m[1])
    if len(m) == 5:
        repeat = m[4]
        log('p_m_play: %s (%s)' % (buf, m[4]))
    else:
        repeat = 1
        log('p_m_play: %s' % buf)
    for i in range(0, repeat):
        sonido = pygame.mixer.Sound(buf)
        canal = sonido.play()
        canal.set_endevent(FIN_PLAY)
        
        termino = False
        while not termino:
            for event in pygame.event.get():
                if event.type == FIN_PLAY:
                    termino = True
    m[0] = m[1]

def p_m_reduce_expand(m):
    '''m : buffer '.' REDUCE par
         | buffer '.' REDUCE
         | buffer '.' EXPAND par
         | buffer '.' EXPAND'''
    l = config.BEAT * int(m[4]) if len(m) == 5 else config.BEAT
    if ((m[3] == 'reduce') and (l < len(m[1]))) or \
       ((m[3] == 'expand') and (l > len(m[1]))):
        m[0] = resample(m[1], l)
    else:
        m[0] = m[1]
    log('p_m_%s: resample(%s, %s) = %s' % (m[3], m[1], l, m[0]))

def p_g(g):
    '''g : SIN par2
         | SIN par
         | LIN par2
         | NOI par
         | NOI
         | SIL'''
    if g[1][:3] == 'sin':
        g[0] = bcSin(g[2]) if type(g[2]) is int else bcSin(g[2][0] , g[2][1])
        log('p_g: sin(%s)' % (g[2]))
    if g[1][:3] == 'lin':
        g[0] = lin(g[2][0] , g[2][1])
        log('p_g: lin(%s, %s)' % (g[2][0],g[2][1]))
    if g[1][:3] == 'noi':
        if len(g) == 3:
            g[0] = noi(g[2])
            log('p_g: noi(%s)' % g[2])
        else:
            g[0] = noi()
            log('p_g: noi')
    if g[1][:3]=='sil':
        g[0] = sil()
        log('p_g: sil')

def p_par(p):
    '''par : '(' num ')' '''
    p[0] = p[2] if len(p) == 4 else p[3]
    log('p_par %s' % p[2])

def p_num(p):
    '''num : SFLOAT
           | UFLOAT
           | SINT
           | UINT '''
    p[0] = p[1]

def p_snum(p):
    '''snum : SFLOAT
            | SINT 
            | snum MUL num
            | snum DIV num '''
    if len(p) == 2:
        p[0] = p[1] 
    else:
        p[0] = p[1] * p[3] if p[2]=='*' else p[1] / p[3]

def p_par2(p):
    '''par2 : '(' num ',' num ')' '''
    p[0] = array([p[2],p[4]], dtype = float)
    log('p_par2 (%s, %s)' % (p[2], p[4]))

def p_m_post(m):
    ''' m : buffer '.' POST'''
    m[0] = m[1]
    print(' '.join(
        map(
            lambda x: str(round(x, 2)),
            m[1] if type(m[1]) is not int else array([m[1]]))
        )
    )
    log('p_m_post: %s' % m[1])

def p_m_loop(m):
    '''m : buffer '.' LOOP par'''
    l = m[4]
    m[0] = resize(m[1], int(len(m[1]) * l))
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
