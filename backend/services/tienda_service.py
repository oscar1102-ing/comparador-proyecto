import repositories.tienda_repository as tienda_repository

def crear_tienda(datos):
    return tienda_repository.crear_tienda(datos)

def obtener_tienda(nombre: str):

    tienda = tienda_repository.obtener_tienda_por_nombre(nombre)

    return tienda

def listar_tiendas():

    tiendas = tienda_repository.obtener_todas_tiendas()

    return tiendas

def verificar_tienda_existe(nombre: str):

    tienda = tienda_repository.obtener_tienda_nombre(nombre)

    if tienda:
        return True
    else:
        return False
