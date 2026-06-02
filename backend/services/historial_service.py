from repositories import historial_repository
from services.plan_service import LIMITES, obtener_limites
from database import conectar_base
 
# ============================================
# OBTENER ROL DEL USUARIO
# ============================================
def _obtener_rol(usuario_id: int) -> str:
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        fila = cursor.fetchone()
        return fila[0] if fila else "usuario"
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# GUARDAR BÚSQUEDA (respetando límite del rol)
# ============================================
def guardar_busqueda(usuario_id: int, busqueda: str):
    if not busqueda.strip():
        return
 
    rol = _obtener_rol(usuario_id)
    limites = obtener_limites(rol)
    limite_historial = limites["historial"]  # None = ilimitado, 10 = gratuito
 
    historial_repository.guardar_busqueda(
        usuario_id,
        busqueda.strip(),
        limite=limite_historial
    )
 
# ============================================
# OBTENER HISTORIAL (respetando límite del rol)
# ============================================
def obtener_historial(usuario_id: int):
    rol = _obtener_rol(usuario_id)
    limites = obtener_limites(rol)
    limite_historial = limites["historial"]  # None = ilimitado
 
    return historial_repository.obtener_historial(usuario_id, limit_count=limite_historial)
 
# ============================================
# ELIMINAR TODO EL HISTORIAL
# ============================================
def eliminar_historial(usuario_id: int):
    return historial_repository.eliminar_historial(usuario_id)
 
# ============================================
# ELIMINAR UNA ENTRADA INDIVIDUAL
# ============================================
def eliminar_entrada(historial_id: int, usuario_id: int):
    return historial_repository.eliminar_entrada(historial_id, usuario_id)
