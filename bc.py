# -----------------------------------------------------------------------------
# bc.py
#
# bc.py es una implementacion de la gramatica para Buffer Colider que es una
# version simplificada del Super Collider.
# -----------------------------------------------------------------------------

import config
from debug import log
from bcGrammar import *

log('Generando la entrada')
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = 'sin(2.1,1.8).play;silence.play(3)'
entrada = '{2;3;4;8}*{1;2;3};{{4;8;6}/2}'
log('Haciendo el parsing')
resultado = yacc.parse(entrada, debug = config.DEBUG == config.DEBUG_FULL)

log('Fin')
