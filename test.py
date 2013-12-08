from sys import argv
from glob import glob
import os.path

ejemplos = glob('ejemplos/*/*buf')

def mostrarUso():
    print 'Uso: python %s <archivo>' % argv[0]
    print 'Ejemplos disponibles:\n\t%s' % '\n\t'.join(ejemplos)

def run(testCallback):
    if len(argv) != 2:
        mostrarUso()
    elif os.path.isfile(argv[1]):
        archivo = open(argv[1], 'r')
        entrada = archivo.read()
        print '----------------------------------------------------'
        print '                  Cadena a procesar'
        print '----------------------------------------------------'
        print entrada
        print '----------------------------------------------------'
        testCallback(entrada)
        archivo.close()
    else:
        print 'El archivo %s no existe' % argv[1]
        mostrarUso()
