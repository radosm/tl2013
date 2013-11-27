import ply.yacc as yacc
from bcTokens import *
from numpy import *
import pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=4096)
SONG_END = pygame.USEREVENT + 1
from debug import log

# Reglas de parsing

precedence = (
    ('left', ';'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'), # UMINUS = Unary Minus
    ('left', '.')
)

# Diccionario de nombres
names = {}

def p_buffer_llaves(b):
    '''buffer : '{' buffer '}' '''
    b[0] = b[2]

def p_buffer_concat(b):
    '''buffer : buffer ';' buffer'''
    b[0] = hstack((b[1], b[3]))
    log('p_buffer_concat %s;%s = %s' % (b[1], b[3], b[0]))

def p_buffer_sum(b):
    '''buffer : buffer '+' buffer'''
    b[0] = b[1] + b[3]
    log('p_buffer_sum: %s + %s = %s' % (b[1], b[3], b[0]))

def p_buffer_res(b):
    '''buffer : buffer '-' buffer'''
    b[0] = b[1] - b[3]
    log('p_buffer_res: %s - %s = %s' % (b[1], b[3], b[0]))

def p_buffer_mul(b):
    '''buffer : buffer '*' buffer'''
    b[0] = b[1] * b[3]
    log('p_buffer_mul: %s * %s = %s' % (b[1], b[3], b[0]))

def p_buffer_div(b):
    '''buffer : buffer '/' buffer'''
    b[0] = b[1] / b[3]
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
    canal = sonido.play()
    canal.set_endevent(SONG_END)
    
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                return

def p_g(g):
    '''g : SIN par2
         | SIL'''
    g[0] = array([333]) if g[1][:3] == 'sil' else array([444]) # reemplazar por sin (par1, par2)
    log('p_g: %s' % g[0])

def p_par(p):
    '''par : '(' UINT ')'
            | '(' FLOAT ')' '''
    p[0] = p[2]
    log('p_par %s' % p[2])

def p_par2(p):
    '''par2 : '(' FLOAT ',' FLOAT ')' '''
    p[0] = (p[2], p[4])
    log('p_par2 (%s, %s)' % (p[2], p[4]))

def p_error(t):
    log("Error de sintaxis en: '%s'" % t.value)

yacc.yacc()
