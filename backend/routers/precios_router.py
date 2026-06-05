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
import repositories.usuario_repository as usuario_repo
import repositories.sede_repository as sede_repo
import services.plan_service as plan_service

router = APIRouter()

# ── PRODUCTOS ──
@router.get("/productos")
def obtener_productos(q: str = "", categoria: str = "", pagina: int = 1, 
                      por_pagina: int = 10, tienda: str = "", 
                      precio_min: str = "", precio_max: str = ""):
    return precio_service.comparar_precios_producto(
        q, categoria, pagina, por_pagina, tienda, precio_min, precio_max
    )

@router.get("/productos/top")
def top_productos():
    return precio_service.obtener_top_productos()

@router.post("/productos")
def crear_producto(datos: ProductoCrear):
    return producto_service.crear_producto(datos)

@router.put("/productos/{id}")
def actualizar_producto(id: int, datos: ProductoActualizar):
    return producto_service.actualizar_producto(iad, datos)

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
    
@router.post("/reenviar-codigo")
def reenviar_codigo(datos: dict):
    usuario_id = datos.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Faltan datos")
    resultado = usuario_service.reenviar_codigo(usuario_id)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
    
@router.delete("/admin/usuarios/{id}")
def eliminar_usuario(id: int):
    resultado = usuario_repo.eliminar_usuario(id)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado


@router.put("/admin/usuarios/{id}/rol")
def cambiar_rol_usuario(id: int, datos: dict):
    nuevo_rol = datos.get("rol")
    if not nuevo_rol:
        raise HTTPException(status_code=400, detail="Falta el rol")
    resultado = usuario_repo.cambiar_rol(id, nuevo_rol)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
    
@router.get("/sedes/{nombre_tienda}")
def obtener_sedes(nombre_tienda: str):
    return sede_repo.obtener_sedes_por_tienda(nombre_tienda)

@router.post("/sedes/multiples")
def obtener_sedes_multiples(datos: dict):
    tiendas = datos.get("tiendas", [])
    if not tiendas:
        return []
    return sede_repo.obtener_sedes_por_tiendas(tiendas)
    
@router.post("/comparaciones/verificar")
def verificar_comparacion(datos: dict):
    usuario_id = datos.get("usuario_id")
    if not usuario_id:
        raise HTTPException(status_code=400, detail="Falta usuario_id")
    resultado = plan_service.verificar_comparacion(usuario_id)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
 
@router.get("/plan/{usuario_id}")
def obtener_plan(usuario_id: int):
    resultado = plan_service.obtener_info_plan(usuario_id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado
    
@router.delete("/historial/entrada/{historial_id}")
def eliminar_entrada_historial(historial_id: int, usuario_id: int):
    resultado = historial_service.eliminar_entrada(historial_id, usuario_id)
    if "error" in resultado:
        raise HTTPException(status_code=404, detail=resultado["error"])
    return resultado
    
    
@router.post("/plan/solicitar")
def endpoint_solicitar_plan(datos: dict):
    usuario_id = datos.get("usuario_id")
    plan = datos.get("plan")
    if not usuario_id or not plan:
        raise HTTPException(status_code=400, detail="Faltan datos")
    resultado = plan_service.solicitar_plan(usuario_id, plan)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
 
 
@router.get("/usuarios/{usuario_id}")
def obtener_usuario_por_id(usuario_id: int):
    from database import conectar_base
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, email, rol FROM usuarios WHERE id = %s", (usuario_id,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    if not fila:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": fila[0],
        "nombre": fila[1],
        "email": fila[2],
        "rol": fila[3]
    }
    
@router.get("/admin/estadisticas")
def obtener_estadisticas():
    from database import conectar_base
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        # Usuarios por plan
        cursor.execute("""
            SELECT rol, COUNT(*) 
            FROM usuarios 
            GROUP BY rol 
            ORDER BY COUNT(*) DESC
        """)
        usuarios_por_plan = [{"plan": r[0], "total": r[1]} for r in cursor.fetchall()]

        # Comparaciones totales por plan
        cursor.execute("""
            SELECT rol, SUM(comparaciones_mes) as total_comparaciones
            FROM usuarios
            GROUP BY rol
            ORDER BY total_comparaciones DESC
        """)
        comparaciones_por_plan = [{"plan": r[0], "total": int(r[1] or 0)} for r in cursor.fetchall()]

        # Top usuarios por comparaciones
        cursor.execute("""
            SELECT nombre, rol, comparaciones_mes
            FROM usuarios
            ORDER BY comparaciones_mes DESC
            LIMIT 5
        """)
        top_usuarios = [{"nombre": r[0], "plan": r[1], "comparaciones": r[2]} for r in cursor.fetchall()]

        # Total comparaciones hoy
        cursor.execute("SELECT SUM(comparaciones_mes) FROM usuarios")
        total_comparaciones = int(cursor.fetchone()[0] or 0)

        return {
            "usuarios_por_plan": usuarios_por_plan,
            "comparaciones_por_plan": comparaciones_por_plan,
            "top_usuarios": top_usuarios,
            "total_comparaciones": total_comparaciones,
            "total_usuarios": sum(p["total"] for p in usuarios_por_plan)
        }
    finally:
        cursor.close()
        conexion.close()
        
@router.get("/admin/estadisticas/tiempo")
def estadisticas_tiempo():
    from database import conectar_base
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        # Comparaciones por día (últimos 30 días)
        cursor.execute("""
            SELECT DATE(fecha) as dia, COUNT(*) as total, plan
            FROM historial_comparaciones
            WHERE fecha >= NOW() - INTERVAL '30 days'
            GROUP BY DATE(fecha), plan
            ORDER BY dia ASC
        """)
        por_dia = [{"dia": str(r[0]), "total": r[1], "plan": r[2]} for r in cursor.fetchall()]

        # Comparaciones por mes (últimos 6 meses)
        cursor.execute("""
            SELECT TO_CHAR(fecha, 'YYYY-MM') as mes, COUNT(*) as total, plan
            FROM historial_comparaciones
            WHERE fecha >= NOW() - INTERVAL '6 months'
            GROUP BY TO_CHAR(fecha, 'YYYY-MM'), plan
            ORDER BY mes ASC
        """)
        por_mes = [{"mes": r[0], "total": r[1], "plan": r[2]} for r in cursor.fetchall()]

        # Nuevos usuarios por día (últimos 30 días)
        cursor.execute("""
            SELECT DATE(fecha_registro) as dia, rol, COUNT(*) as total
            FROM usuarios
            WHERE fecha_registro >= NOW() - INTERVAL '30 days'
            GROUP BY DATE(fecha_registro), rol
            ORDER BY dia ASC
        """)
        usuarios_por_dia = [{"dia": str(r[0]), "plan": r[1], "total": r[2]} for r in cursor.fetchall()]

        return {
            "comparaciones_por_dia": por_dia,
            "comparaciones_por_mes": por_mes,
            "usuarios_por_dia": usuarios_por_dia
        }
    finally:
        cursor.close()
        conexion.close()
        
@router.put("/usuarios/{usuario_id}/actualizar")
def actualizar_perfil(usuario_id: int, datos: dict):
    resultado = usuario_service.actualizar_perfil(usuario_id, datos)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado
