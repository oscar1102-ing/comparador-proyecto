from fastapi import APIRouter, HTTPException
import services.precio_service as precio_service
import services.usuario_service as usuario_service
import services.producto_service as producto_service
import services.favorito_service as favorito_service
import services.tienda_service as tienda_service
import services.historial_service as historial_service
from models.usuario_model import UsuarioRegistro, UsuarioLogin
from models.producto_model import ProductoCrear, ProductoActualizar
from models.favorito_model import FavoritoCrear
from models.tienda_model import TiendaCrear
from models.mfa_model import VerificarMFA
from database import conectar_base

router = APIRouter()

# ── PRODUCTOS ──
@router.get("/productos")
def obtener_productos(q: str = "", pagina: int = 1, por_pagina: int = 10):
    return precio_service.comparar_precios_producto(q, pagina, por_pagina)

@router.get("/productos/top")
def top_productos():
    return precio_service.obtener_top_productos()

@router.post("/productos")
def crear_producto(datos: ProductoCrear):
    return producto_service.crear_producto(datos)

@router.put("/productos/{id}")
def actualizar_producto(id: int, datos: ProductoActualizar):
    return producto_service.actualizar_producto(id, datos)

@router.delete("/productos/{id}")
def eliminar_producto(id: int):
    return producto_service.eliminar_producto(id)

@router.get("/producto")
def detalle_producto(nombre: str):
    return precio_service.obtener_detalle_producto(nombre)

# ── USUARIOS ──
@router.post("/registro")
def registrar_usuario(datos: UsuarioRegistro):
    resultado = usuario_service.registrar_usuario(datos)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@router.post("/login")
def login(datos: UsuarioLogin):
    resultado = usuario_service.login(datos)
    if "error" in resultado:
        raise HTTPException(status_code=401, detail=resultado["error"])
    return resultado

@router.post("/verificar-mfa")
def verificar_mfa_endpoint(datos: VerificarMFA):
    resultado = usuario_service.verificar_mfa(datos.usuario_id, datos.codigo)
    if "error" in resultado:
        raise HTTPException(status_code=401, detail=resultado["error"])
    return resultado

# ── FAVORITOS ──
@router.post("/favoritos/toggle")
def toggle_favorito(datos: FavoritoCrear):
    resultado = favorito_service.toggle_favorito(datos.usuario_id, datos.producto_id)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@router.post("/favoritos")
def agregar_favorito(datos: FavoritoCrear):
    resultado = favorito_service.agregar_favorito(datos.usuario_id, datos.producto_id)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@router.get("/favoritos/{usuario_id}")
def obtener_favoritos(usuario_id: int):
    return favorito_service.obtener_favoritos(usuario_id)

@router.delete("/favoritos/{favorito_id}")
def eliminar_favorito(favorito_id: int, usuario_id: int):
    resultado = favorito_service.eliminar_favorito(favorito_id, usuario_id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado

# ── HISTORIAL ──
@router.post("/historial/guardar")
def guardar_busqueda(datos: dict):
    usuario_id = datos.get("usuario_id")
    busqueda = datos.get("busqueda")
    if not usuario_id or not busqueda:
        raise HTTPException(status_code=400, detail="Faltan datos")
    historial_service.guardar_busqueda(usuario_id, busqueda)
    return {"mensaje": "ok"}

@router.get("/historial/usuario/{usuario_id}")
def obtener_historial_usuario(usuario_id: int):
    return historial_service.obtener_historial(usuario_id)

@router.delete("/historial/usuario/{usuario_id}")
def eliminar_historial(usuario_id: int):
    return historial_service.eliminar_historial(usuario_id)

# ── TIENDAS ──
@router.post("/tiendas")
def crear_tienda(datos: TiendaCrear):
    return tienda_service.crear_tienda(datos)

@router.get("/tiendas")
def obtener_tiendas():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM tiendas ORDER BY nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": f[0], "nombre": f[1]} for f in filas]

# ── CATEGORIAS Y MARCAS ──
@router.get("/categorias")
def obtener_categorias():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": f[0], "nombre": f[1]} for f in filas]

@router.get("/marcas")
def obtener_marcas():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM marcas ORDER BY nombre")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": f[0], "nombre": f[1]} for f in filas]

# ── ADMIN ──
@router.get("/admin/usuarios")
def listar_usuarios():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, email, rol, fecha_registro FROM usuarios ORDER BY id")
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": f[0], "nombre": f[1], "email": f[2], "rol": f[3], "fecha_registro": str(f[4])} for f in filas]
