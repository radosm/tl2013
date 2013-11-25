from bcGrammar import *

print 'Generando la entrada'
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = '{2;4;5}.play(4.3).play'
print 'Haciendo el parsing'
resultado = yacc.parse(entrada)

print 'Fin'
