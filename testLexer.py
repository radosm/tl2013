from sys import argv
from bcTokens import lexer
from glob import glob
import os.path

def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print tok

def mostrarUso():
    print 'Uso: python %s <archivo>' % argv[0]
    print 'Ejemplos disponibles: %s' % ejemplos

ejemplos = glob('examples/*buf')
if len(argv) != 2:
    mostrarUso()
elif os.path.isfile(argv[1]):
    archivo = open(argv[1], 'r')
    test(archivo.read())
    archivo.close()
else:
    print 'El archivo %s no existe' % argv[1]
    mostrarUso()
