import ply.yacc as yacc
from bcTokens import *
from numpy import *
import pygame
pygame.init()
pygame.mixer.init(frequency=44100,size=-16,channels=1,buffer=4096)
SONG_END = pygame.USEREVENT + 1

# Reglas de parsing

precedence = (
    ('left', 'CONCAT'),
    ('left', 'DOT')
)

# Diccionario de nombres
names = {}

def p_buffer_brackets(t):
    '''buffer : '{' buffer '}' '''
    t[0] = t[2]

def p_buffer_play(t):
    '''buffer : buffer DOT PLAY PARFLOAT
              | buffer DOT PLAY'''
    print t[4]
    t[0] = t[1]
    print 'p_buffer_play: %s' % t[1]
    buf = array(t[1])
    sonido = pygame.mixer.Sound(buf)
    canal = sonido.play()
    canal.set_endevent(SONG_END)
    
    while True:
        for event in pygame.event.get():
            if event.type == SONG_END:
                return

def p_buffer_concat(t):
    'buffer : buffer CONCAT buffer'
    print 'p_buffer_concat %s;%s' % (t[1],t[3])
    t[0] = t[1] + t[3]

def p_buffer_int(t):
    'buffer : INT'
    print 'p_buffer_int: %s' % t[1]
    t[0] = [t[1]]



def p_error(t):
    print "Error de sintaxis en: '%s'" % t.value

yacc.yacc()
