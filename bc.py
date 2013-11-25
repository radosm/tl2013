from bcGrammar import *

print 'Generando la entrada'
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = 'sin(2.1,1.8).play;silence'
print 'Haciendo el parsing'
resultado = yacc.parse(entrada)

print 'Fin'
