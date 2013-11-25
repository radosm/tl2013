import ply.yacc as yacc
from bcTokens import *
from numpy import *
import pygame
pygame.init()
pygame.mixer.init(frequency=44100,size=-16,channels=1,buffer=4096)
SONG_END = pygame.USEREVENT + 1
from debug import log

# Reglas de parsing

precedence = (
    ('left', '+'),
    ('left', 'CONCAT'),
    ('left', 'DOT')
)

# Diccionario de nombres
names = {}

def p_buffer_brackets(t):
    '''buffer : '{' buffer '}' '''
    t[0] = t[2]

def p_buffer_concat(t):
    'buffer : buffer CONCAT buffer'
    t[0] = hstack((t[1], t[3]))
    log('p_buffer_concat %s;%s = %s' % (t[1], t[3], t[0]))

def p_buffer_sum(t):
    '''buffer : buffer '+' buffer'''
    t[0] = t[1] + t[3]
    log('p_buffer_sum: %s + %s = %s' % (t[1], t[3], t[0]))

def p_buffer_int(t):
    'buffer : INT'
    log('p_buffer_int: %s' % t[1])
    t[0] = array([t[1]])

def p_buffer_m(t):
    'buffer : m'
    log('p_buffer_m: %s' % t[1])
    t[0] = t[1]

def p_buffer_g(t):
    'buffer : g'
    log('p_buffer_g: %s' % t[1])
    t[0] = t[1]

def p_m_play(t):
    '''m : buffer DOT PLAY par
         | buffer DOT PLAY'''
    t[0] = t[1]
    if len(t) == 5:
        log('p_m_play: %s (%s)' % (t[1], t[4]))
    else:
        log('p_m_play: %s' % t[1])
    sonido = pygame.mixer.Sound(t[1])
    canal = sonido.play()
    canal.set_endevent(SONG_END)
    
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                return

def p_g(t):
    '''g : SIN par2
         | SIL'''
    log('p_g: %s' % t[0])
    t[0] = array([333]) if t[1] == 'sil' else array([444]) # reemplazar por sin (par1, par2)

def p_par(t):
    '''par : '(' INT ')'
            | '(' FLOAT ')' '''
    log('p_par %s' % t[2])
    t[0] = t[2]

def p_par2(t):
    '''par2 : '(' FLOAT ',' FLOAT ')' '''
    log('p_par2 (%s, %s)' % (t[2], t[4]))
    t[0] = (t[2], t[4])


def p_error(t):
    log("Error de sintaxis en: '%s'" % t.value)

yacc.yacc()
