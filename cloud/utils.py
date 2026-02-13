#directorio raiz
CLOUD_DIR = '/srv/cloud/'

#plantillas 
ERRORTEMPLATE = "error.html"

#contextos de error 404 y 500
INVALIDLOGIN = {
        'title':"error",
        'code':404,
        'summary':"Acceso invalido",
        'description':"El nombre de usuario o contraseña son incorrectos o no existen"
}

INTERNALERROR = {
    'title':"error",
    'code':500,
    'summary':"fallo interno del servidor",
    'description':"Ocurrio un fallo inseperado durante la transaccion ejecutada"
}

NOTFOUNDDIR = {
        'title':"error",
        'code':404,
        'summary':"directorio no entontrado",
        'description':"El nombre del directorio es incorrecto o no existe"
}

NOTFOUNDFILE = {
    'title':"error",
    'code':404,
    'summary':"directorio no entontrado",
    'description':"El nombre del directorio es incorrecto o no existe"
}