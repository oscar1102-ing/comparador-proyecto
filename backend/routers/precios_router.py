from fastapi import APIRouter
import services.precio_service as precio_service

router = APIRouter()

@router.get("/productos")
def obtener_productos(q: str = ""):
    
    resultado = precio_service.comparar_precios_producto(q)

    return resultado

@router.get("/productos/top")
def top_productos():
    resultado = precio_service.obtener_top_productos()

    return resultado







@router.get("/historial/{producto}")
def obtener_historial(producto: str):

    resultado = precio_service.obtener_historial_producto(producto)

    return resultado




@router.get("/producto")
def detalle_producto(nombre: str):
    return precio_service.obtener_detalle_producto(nombre)