from sys import argv
from glob import glob
import os.path

ejemplos = glob('ejemplos/*/*buf')

def mostrarUso():
    print 'Uso: python  %s [-OPCION] <archivo>' % argv[0]
    print 'Descripcion'
    print '\t  -f \t Con esta opcion podes pasarle un archivo con buffers.'
    print '\t  -i \t Con esta opcion podes pasarle los buffers por consola.'
    print 'Ejemplos disponibles:\n\t%s' % '\n\t'.join(ejemplos)

def run(testCallback):
    if not ((len(argv) == 2 and argv[1] == '-i') or 
            (len(argv) == 3 and argv[1] == '-f')): 
        mostrarUso()
    elif  len(argv) == 3 and argv[1] == '-f':
        if os.path.isfile(argv[2]):
            archivo = open(argv[2], 'r')
            entrada = archivo.read()
            print '----------------------------------------------------'
            print '                  Cadena a procesar'
            print '----------------------------------------------------'
            print entrada
            print '----------------------------------------------------'
            testCallback(entrada)
            archivo.close()
        else:
            print 'El archivo %s no existe' % argv[2]
    elif len(argv) == 2 and argv[1] == '-i':
        print 'q para salir \n'
        while True:
            entrada = raw_input(">> ")
            if entrada == 'q':
                print 'Chau'
                break
            testCallback(entrada)
    else:
        mostrarUso()



