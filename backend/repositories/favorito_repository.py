from database import conectar_base
from services.plan_service import verificar_favorito
 
# ============================================
# TOGGLE FAVORITO (con límite por plan)
# ============================================
def toggle_favorito(usuario_id: int, producto_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        # Verificar si ya existe
        cursor.execute("""
            SELECT id FROM favoritos
            WHERE usuario_id = %s AND producto_id = %s
        """, (usuario_id, producto_id))
        existente = cursor.fetchone()
 
        if existente:
            # Ya existe — eliminar
            cursor.execute("DELETE FROM favoritos WHERE id = %s", (existente[0],))
            conexion.commit()
            return {"accion": "eliminado"}
        else:
            # No existe — verificar límite antes de agregar
            verificacion = verificar_favorito(usuario_id)
            if "error" in verificacion:
                return {"error": verificacion["error"]}
            if not verificacion["permitido"]:
                return {
                    "error": verificacion["mensaje"],
                    "limite_alcanzado": True,
                    "limite": verificacion["limite"]
                }
 
            cursor.execute("""
                INSERT INTO favoritos (usuario_id, producto_id)
                VALUES (%s, %s)
            """, (usuario_id, producto_id))
            conexion.commit()
            return {"accion": "agregado"}
 
    except Exception as e:
        conexion.rollback()
        print(f"Error toggle favorito: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# AGREGAR FAVORITO
# ============================================
def agregar_favorito(usuario_id: int, producto_id: int):
    verificacion = verificar_favorito(usuario_id)
    if "error" in verificacion:
        return {"error": verificacion["error"]}
    if not verificacion["permitido"]:
        return {
            "error": verificacion["mensaje"],
            "limite_alcanzado": True
        }
 
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO favoritos (usuario_id, producto_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING
        """, (usuario_id, producto_id))
        conexion.commit()
        return {"mensaje": "Favorito agregado"}
    except Exception as e:
        conexion.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# OBTENER FAVORITOS
# ============================================
def obtener_favoritos(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT f.id, p.id, p.nombre, p.imagen_url,
                   MIN(pr.precio) as precio_min
            FROM favoritos f
            JOIN productos p ON f.producto_id = p.id
            LEFT JOIN precios pr ON pr.producto_id = p.id
            WHERE f.usuario_id = %s
            GROUP BY f.id, p.id, p.nombre, p.imagen_url
            ORDER BY f.id DESC
        """, (usuario_id,))
        filas = cursor.fetchall()
        return [
            {
                "favorito_id": f[0],
                "producto_id": f[1],
                "nombre": f[2],
                "imagen": f[3],
                "precio": f[4]
            }
            for f in filas
        ]
    except Exception as e:
        print(f"Error obteniendo favoritos: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# ELIMINAR FAVORITO
# ============================================
def eliminar_favorito(favorito_id: int, usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            DELETE FROM favoritos
            WHERE id = %s AND usuario_id = %s
        """, (favorito_id, usuario_id))
        if cursor.rowcount == 0:
            return {"error": "Favorito no encontrado"}
        conexion.commit()
        return {"mensaje": "Favorito eliminado"}
    except Exception as e:
        conexion.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
