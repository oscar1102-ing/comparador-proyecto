from database import conectar_base

def guardar_busqueda(usuario_id: int, busqueda: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO historial_busquedas (usuario_id, busqueda, fecha_busqueda)
        VALUES (%s, %s, NOW())
    """, (usuario_id, busqueda))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_historial(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, busqueda, fecha_busqueda
        FROM historial_busquedas
        WHERE usuario_id = %s
        ORDER BY fecha_busqueda DESC
        LIMIT 50
    """, (usuario_id,))
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [{"id": f[0], "busqueda": f[1], "fecha": str(f[2])} for f in resultado]

def eliminar_historial(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM historial_busquedas WHERE usuario_id = %s", (usuario_id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Historial eliminado"}
