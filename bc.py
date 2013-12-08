# -----------------------------------------------------------------------------
# bc.py
#
# bc.py es una implementacion de la gramatica para Buffer Colider que es una
# version simplificada del Super Collider.
# -----------------------------------------------------------------------------

import config
from debug import log
from bcGrammar import *
import test

def testCallback(data):
    log('Parseando la entrada')
    yacc.parse(data, debug = config.DEBUG == config.DEBUG_FULL)
    log('Fin')

test.run(testCallback)



