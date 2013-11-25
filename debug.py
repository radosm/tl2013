NONE = 0
SIMPLE = 1
FULL = 2
habilitado = NONE

def log(mensaje):
    if habilitado != NONE:
        print (mensaje)
