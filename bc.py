# -----------------------------------------------------------------------------
# bc.py
#
# bc.py es una implementacion de la gramatica para Buffer Colider que es una
# version simplificada del Super Collider.
# -----------------------------------------------------------------------------

import debug
from debug import log
from bcGrammar import *

debug.habilitado = debug.SIMPLE

log('Generando la entrada')
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = 'sin(2.1,1.8).play;silence.play(3)'
#entrada = '{3+21;4}-{2;1};5'
log('Haciendo el parsing')
resultado = yacc.parse(entrada, debug = debug.habilitado == debug.FULL)

log('Fin')
