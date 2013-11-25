from bcGrammar import *

print 'Generando la entrada'
#valores = range(8,15)
#entrada = ';'.join(map(lambda x: str(x), valores)) + '.play'

entrada = '{{1;2;3};{3;4;5}}.play(4.3)'
print 'Haciendo el parsing'
resultado = yacc.parse(entrada)

print 'Fin'
