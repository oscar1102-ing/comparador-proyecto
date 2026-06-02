from database import conectar_base
 
# ============================================
# LIMITES POR ROL
# ============================================
LIMITES = {
    "usuario": {
        "favoritos": 5,
        "comparaciones_mes": 5,
        "historial": 10,
        "alertas": 0,
    },
    "basico": {
        "favoritos": 50,
        "comparaciones_mes": 20,
        "historial": None,  # ilimitado
        "alertas": 3,
    },
    "pro": {
        "favoritos": None,  # ilimitado
        "comparaciones_mes": None,  # ilimitado
        "historial": None,
        "alertas": None,
    },
    "admin": {
        "favoritos": None,
        "comparaciones_mes": None,
        "historial": None,
        "alertas": None,
    },
    "root": {
        "favoritos": None,
        "comparaciones_mes": None,
        "historial": None,
        "alertas": None,
    },
}
 
def obtener_limites(rol: str):
    return LIMITES.get(rol, LIMITES["usuario"])
 
# ============================================
# VERIFICAR Y CONTAR COMPARACION
# ============================================
def verificar_comparacion(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT rol, comparaciones_mes, comparaciones_reset
            FROM usuarios WHERE id = %s
        """, (usuario_id,))
        fila = cursor.fetchone()
 
        if not fila:
            return {"error": "Usuario no encontrado"}
 
        rol, comparaciones_mes, comparaciones_reset = fila
        limites = obtener_limites(rol)
 
        # Resetear contador si cambió el mes
        from datetime import date
        hoy = date.today()
        if comparaciones_reset.month != hoy.month or comparaciones_reset.year != hoy.year:
            cursor.execute("""
                UPDATE usuarios
                SET comparaciones_mes = 0, comparaciones_reset = %s
                WHERE id = %s
            """, (hoy, usuario_id))
            conexion.commit()
            comparaciones_mes = 0
 
        limite = limites["comparaciones_mes"]
 
        # Si es ilimitado (pro, admin, root)
        if limite is None:
            cursor.execute("""
                UPDATE usuarios SET comparaciones_mes = comparaciones_mes + 1 WHERE id = %s
            """, (usuario_id,))
            conexion.commit()
            return {"permitido": True, "usadas": comparaciones_mes + 1, "limite": None}
 
        # Si llegó al límite
        if comparaciones_mes >= limite:
            return {
                "permitido": False,
                "usadas": comparaciones_mes,
                "limite": limite,
                "mensaje": f"Alcanzaste el límite de {limite} comparaciones este mes. Mejora tu plan para ver más."
            }
 
        # Contar la comparación
        cursor.execute("""
            UPDATE usuarios SET comparaciones_mes = comparaciones_mes + 1 WHERE id = %s
        """, (usuario_id,))
        conexion.commit()
 
        return {
            "permitido": True,
            "usadas": comparaciones_mes + 1,
            "limite": limite,
            "restantes": limite - (comparaciones_mes + 1)
        }
 
    except Exception as e:
        conexion.rollback()
        print(f"Error verificando comparación: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# VERIFICAR LIMITE DE FAVORITOS
# ============================================
def verificar_favorito(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
        fila = cursor.fetchone()
        if not fila:
            return {"error": "Usuario no encontrado"}
 
        rol = fila[0]
        limites = obtener_limites(rol)
        limite = limites["favoritos"]
 
        # Sin límite
        if limite is None:
            return {"permitido": True, "limite": None}
 
        # Contar favoritos actuales
        cursor.execute(
            "SELECT COUNT(*) FROM favoritos WHERE usuario_id = %s",
            (usuario_id,)
        )
        total = cursor.fetchone()[0]
 
        if total >= limite:
            return {
                "permitido": False,
                "total": total,
                "limite": limite,
                "mensaje": f"Alcanzaste el límite de {limite} favoritos. Mejora tu plan para agregar más."
            }
 
        return {"permitido": True, "total": total, "limite": limite}
 
    except Exception as e:
        print(f"Error verificando favorito: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# OBTENER INFO DEL PLAN DEL USUARIO
# ============================================
def obtener_info_plan(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT rol, comparaciones_mes, comparaciones_reset
            FROM usuarios WHERE id = %s
        """, (usuario_id,))
        fila = cursor.fetchone()
        if not fila:
            return {"error": "Usuario no encontrado"}
 
        rol, comparaciones_mes, comparaciones_reset = fila
        limites = obtener_limites(rol)
 
        # Contar favoritos
        cursor.execute(
            "SELECT COUNT(*) FROM favoritos WHERE usuario_id = %s",
            (usuario_id,)
        )
        total_favoritos = cursor.fetchone()[0]
 
        return {
            "rol": rol,
            "comparaciones_usadas": comparaciones_mes,
            "comparaciones_limite": limites["comparaciones_mes"],
            "favoritos_usados": total_favoritos,
            "favoritos_limite": limites["favoritos"],
            "historial_limite": limites["historial"],
            "alertas_limite": limites["alertas"],
        }
 
    except Exception as e:
        print(f"Error obteniendo info plan: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
