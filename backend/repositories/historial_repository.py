from database import conectar_base
 
# ============================================
# GUARDAR BÚSQUEDA CON LÍMITE POR ROL
# Si el usuario es gratuito y ya tiene 10,
# elimina la más antigua antes de insertar.
# ============================================
def guardar_busqueda(usuario_id: int, busqueda: str, limite: int = None):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        # Evitar duplicados consecutivos
        cursor.execute("""
            SELECT busqueda FROM historial_busquedas
            WHERE usuario_id = %s
            ORDER BY fecha_busqueda DESC
            LIMIT 1
        """, (usuario_id,))
        ultimo = cursor.fetchone()
        if ultimo and ultimo[0].lower() == busqueda.lower():
            return  # No guardar duplicado consecutivo
 
        if limite is not None:
            # Contar cuántas tiene
            cursor.execute("""
                SELECT COUNT(*) FROM historial_busquedas WHERE usuario_id = %s
            """, (usuario_id,))
            total = cursor.fetchone()[0]
 
            # Si ya llegó al límite, eliminar la más antigua
            if total >= limite:
                cursor.execute("""
                    DELETE FROM historial_busquedas
                    WHERE id = (
                        SELECT id FROM historial_busquedas
                        WHERE usuario_id = %s
                        ORDER BY fecha_busqueda ASC
                        LIMIT 1
                    )
                """, (usuario_id,))
 
        cursor.execute("""
            INSERT INTO historial_busquedas (usuario_id, busqueda, fecha_busqueda)
            VALUES (%s, %s, NOW())
        """, (usuario_id, busqueda))
        conexion.commit()
 
    except Exception as e:
        conexion.rollback()
        print(f"Error guardando búsqueda: {e}")
    finally:
        cursor.close()
        conexion.close()
 
 
# ============================================
# OBTENER HISTORIAL
# limit_count: cuántos traer (None = todos)
# ============================================
def obtener_historial(usuario_id: int, limit_count: int = None):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        if limit_count is not None:
            cursor.execute("""
                SELECT id, busqueda, fecha_busqueda
                FROM historial_busquedas
                WHERE usuario_id = %s
                ORDER BY fecha_busqueda DESC
                LIMIT %s
            """, (usuario_id, limit_count))
        else:
            cursor.execute("""
                SELECT id, busqueda, fecha_busqueda
                FROM historial_busquedas
                WHERE usuario_id = %s
                ORDER BY fecha_busqueda DESC
            """, (usuario_id,))
        resultado = cursor.fetchall()
        return [{"id": f[0], "busqueda": f[1], "fecha": str(f[2])} for f in resultado]
    except Exception as e:
        print(f"Error obteniendo historial: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
 
 
# ============================================
# ELIMINAR TODO EL HISTORIAL DE UN USUARIO
# ============================================
def eliminar_historial(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "DELETE FROM historial_busquedas WHERE usuario_id = %s", (usuario_id,)
        )
        conexion.commit()
        return {"mensaje": "Historial eliminado"}
    except Exception as e:
        conexion.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
 
 
# ============================================
# ELIMINAR UNA ENTRADA INDIVIDUAL
# ============================================
def eliminar_entrada(historial_id: int, usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            DELETE FROM historial_busquedas
            WHERE id = %s AND usuario_id = %s
        """, (historial_id, usuario_id))
        if cursor.rowcount == 0:
            return {"error": "Entrada no encontrada"}
        conexion.commit()
        return {"mensaje": "Entrada eliminada"}
    except Exception as e:
        conexion.rollback()
        return {"error": str(e)}
    finally:
        cursor.close()
        conexion.close()
