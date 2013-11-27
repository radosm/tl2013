import config

def log(mensaje):
    if config.DEBUG != config.DEBUG_DESHABILITADO:
        print (mensaje)
