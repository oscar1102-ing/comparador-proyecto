from database import conectar_base

def crear_producto(datos):
    conexion = conectar_base()
    cursor = conexion.cursor()

    # Crear producto
    # DESPUÉS
    consulta_producto = """
    INSERT INTO productos
    (nombre, descripcion, categoria_id, marca_id, imagen_url)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
    """

    valores_producto = (
        datos.nombre,
        datos.descripcion,
        datos.categoria_id,
        datos.marca_id,
        datos.imagen_url
    )

    cursor.execute(consulta_producto, valores_producto)

    # Obtener ID del producto creado
    producto_id = cursor.fetchone()[0]

    # Crear precio
    consulta_precio = """
    INSERT INTO precios
    (producto_id, tienda_id, precio)
    VALUES (%s, %s, %s)
    """

    valores_precio = (
        producto_id,
        datos.tienda_id,
        datos.precio
    )

    cursor.execute(consulta_precio, valores_precio)

    conexion.commit()

    cursor.close()
    conexion.close()

    return {
        "mensaje": "Producto creado correctamente",
        "producto_id": producto_id
    }

def obtener_producto_id(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT id
    FROM productos
    WHERE id = %s
    """

    cursor.execute(consulta,(id,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado

def obtener_producto_nombre(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT nombre
    FROM productos
    WHERE nombre = %s
    """

    cursor.execute(consulta, (nombre,))

    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado

def todos_productos():
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT *
    FROM productos
    """

    cursor.execute(consulta)

    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado

def obtener_producto(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT id, nombre, imagen_url
    FROM productos
    WHERE LOWER(REPLACE(nombre, ' ', '')) = %s
    LIMIT 1
    """

    nombre_normalizado = nombre.lower().strip().replace(" ", "")
    cursor.execute(consulta, (nombre_normalizado,))
    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not fila:
        return None

    return {
        "id": fila[0],
        "nombre": fila[1],
        "imagen": fila[2] or "imagenes/logo1.png"
    }


def obtener_similares(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    palabra = nombre.split(" ")[0].lower()

    consulta = """
    SELECT p.nombre, MIN(pr.precio) as precio
    FROM productos p
    JOIN precios pr ON pr.producto_id = p.id
    WHERE LOWER(p.nombre) LIKE %s
    GROUP BY p.nombre
    LIMIT 5
    """

    cursor.execute(consulta, (f"%{palabra}%",))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    similares = []
    for fila in resultado:
        similares.append({
            "nombre": fila[0],
            "precio": float(fila[1])
        })

    return similares
    
def eliminar_producto(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    # Primero eliminar precios asociados
    cursor.execute("DELETE FROM precios WHERE producto_id = %s", (id,))
    
    # Luego eliminar el producto
    cursor.execute("DELETE FROM productos WHERE id = %s RETURNING id", (id,))
    eliminado = cursor.fetchone()
    
    conexion.commit()
    cursor.close()
    conexion.close()
    
    if not eliminado:
        return {"error": "Producto no encontrado"}
    return {"mensaje": "Producto eliminado"}

def actualizar_producto(id: int, datos):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos 
        SET nombre = %s, descripcion = %s, categoria_id = %s, marca_id = %s
        WHERE id = %s
    """, (datos.nombre, datos.descripcion, datos.categoria_id, datos.marca_id, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Producto actualizado"}
