from sys import argv
from glob import glob
import os.path

ejemplos = glob('examples/*buf')

def mostrarUso():
    print 'Uso: python %s <archivo>' % argv[0]
    print 'Ejemplos disponibles: %s' % ejemplos

def run(testCallback):
    if len(argv) != 2:
        mostrarUso()
    elif os.path.isfile(argv[1]):
        archivo = open(argv[1], 'r')
        testCallback(archivo.read())
        archivo.close()
    else:
        print 'El archivo %s no existe' % argv[1]
        mostrarUso()
