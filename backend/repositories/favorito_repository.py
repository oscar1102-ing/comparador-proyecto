from database import conectar_base

def agregar_favorito(usuario_id: int, producto_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    # Verificar si ya existe
    cursor.execute("""
        SELECT id FROM favoritos 
        WHERE usuario_id = %s AND producto_id = %s
    """, (usuario_id, producto_id))
    
    if cursor.fetchone():
        cursor.close()
        conexion.close()
        return {"error": "Ya está en favoritos"}
    
    cursor.execute("""
        INSERT INTO favoritos (usuario_id, producto_id)
        VALUES (%s, %s)
        RETURNING id
    """, (usuario_id, producto_id))
    
    nuevo_id = cursor.fetchone()[0]
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Agregado a favoritos", "id": nuevo_id}

def obtener_favoritos(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT f.id, p.id, p.nombre, p.imagen_url, MIN(pr.precio) as precio_minimo
        FROM favoritos f
        JOIN productos p ON f.producto_id = p.id
        LEFT JOIN precios pr ON pr.producto_id = p.id
        WHERE f.usuario_id = %s
        GROUP BY f.id, p.id, p.nombre, p.imagen_url
        ORDER BY f.id DESC
    """, (usuario_id,))
    
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    favoritos = []
    for fila in resultado:
        favoritos.append({
            "favorito_id": fila[0],
            "producto_id": fila[1],
            "nombre": fila[2],
            "imagen": fila[3],
            "precio_minimo": float(fila[4]) if fila[4] else None
        })
    return favoritos

def eliminar_favorito(favorito_id: int, usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    cursor.execute("""
        DELETE FROM favoritos 
        WHERE id = %s AND usuario_id = %s
        RETURNING id
    """, (favorito_id, usuario_id))
    
    eliminado = cursor.fetchone()
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if not eliminado:
        return {"error": "Favorito no encontrado"}
    return {"mensaje": "Eliminado de favoritos"}
    
def toggle_favorito(usuario_id: int, producto_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id FROM favoritos 
        WHERE usuario_id = %s AND producto_id = %s
    """, (usuario_id, producto_id))
    
    existente = cursor.fetchone()
    
    if existente:
        cursor.execute("DELETE FROM favoritos WHERE id = %s", (existente[0],))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"accion": "eliminado"}
    else:
        cursor.execute("""
            INSERT INTO favoritos (usuario_id, producto_id)
            VALUES (%s, %s)
        """, (usuario_id, producto_id))
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"accion": "agregado"}
