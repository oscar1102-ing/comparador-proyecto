import repositories.producto_repository as producto_repository

def crear_producto(datos):
    return producto_repository.crear_producto(datos)

def obtener_producto(nombre: str):

    producto = producto_repository.obtener_producto_nombre(nombre)

    return producto

def listar_productos():

    productos = producto_repository.todos_productos()

    return productos

def verificar_producto_existe(nombre: str):

    producto = producto_repository.obtener_producto_nombre(nombre)

    if producto:
        return True
    else:
        return False
    
def obtener_detalle_producto(nombre: str):

    producto = producto_repository.obtener_producto(nombre)
    tiendas = producto_repository.obtener_tiendas_producto(nombre)
    similares = producto_repository.obtener_similares(nombre)

    return {
        "producto": producto,
        "tiendas": tiendas,
        "similares": similares
    }
    
def eliminar_producto(id: int):
    return producto_repository.eliminar_producto(id)

def actualizar_producto(id: int, datos):
    return producto_repository.actualizar_producto(id, datos)
