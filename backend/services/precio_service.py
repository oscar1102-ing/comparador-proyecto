from repositories import producto_repository
from repositories import tienda_repository
from repositories import precio_repository
import services.producto_service as producto_service
import services.tienda_service as tienda_service

def registrar_precio(producto, tienda, precio):

    prod = producto_repository.obtener_producto_nombre(producto)

    if not prod:
        return {"error": "producto no existe"}

    tienda_db = tienda_repository.obtener_tienda_nombre(tienda)

    if not tienda_db:
        return {"error": "tienda no existe"}

    id_producto = prod[0]
    id_tienda = tienda_db[0]

    return precio_repository.guardar_precio(id_producto, id_tienda, precio)

def comparar_precios_producto(producto: str):

    precios = precio_repository.obtener_precios_producto(producto)

    return precios


def obtener_top_productos():
    return precio_repository.obtener_productos_top()


def obtener_detalle_producto(nombre: str):

    producto = producto_repository.obtener_producto(nombre)
    tiendas = tienda_repository.obtener_tiendas_producto(nombre)
    similares = producto_repository.obtener_similares(nombre)

    return {
        "producto": producto,
        "tiendas": tiendas,
        "similares": similares
    }









def obtener_historial_producto(producto: str):

    historial = precio_repository.obtener_historial_precios(producto)

    return historial



def obtener_precios_por_producto(nombre):
    return precio_repository.obtener_precios(nombre)


def obtener_productos_similares(nombre):
    return precio_repository.obtener_similares(nombre)

