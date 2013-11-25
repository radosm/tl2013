import debug
from debug import log
from bcGrammar import *

debug.habilitado = debug.SIMPLE

log('Generando la entrada')
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = 'sin(2.1,1.8).play;silence'
entrada = '3+21'
log('Haciendo el parsing')
resultado = yacc.parse(entrada, debug = debug.habilitado == debug.FULL)

log('Fin')
