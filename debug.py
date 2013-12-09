import config
import traceback

def log(mensaje):
    if config.DEBUG != config.DEBUG_DESHABILITADO:
        print (mensaje)

def errorTipos(mensaje):
    if config.chequearTipos:
        traceback.print_stack()
        print '==> %s' % mensaje
        exit('Podes deshabilitar el chequeo de tipos cambiando en la configuracion la opcion chequearTipos')
