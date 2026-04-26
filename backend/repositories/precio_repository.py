from database import conectar_base

def guardar_precio(producto_id, tienda_id, precio):

    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    INSERT INTO precios(producto_id, tienda_id, precio, fecha_actual)
    VALUES(%s,%s,%s,NOW())
    """

    cursor.execute(consulta,(producto_id, tienda_id, precio))

    conexion.commit()

    cursor.close()
    conexion.close()

def obtener_productos_top():
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT p.nombre, t.nombre, pr.precio
    FROM precios pr
    JOIN productos p ON pr.producto_id = p.id_producto
    JOIN tiendas t ON pr.tienda_id = t.id_tienda
    ORDER BY pr.precio ASC
    LIMIT 10
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    productos = []
    for fila in resultado:
        productos.append({
            "nombre": fila[0],
            "tienda": fila[1],
            "precio": float(fila[2]),
            "imagen": "https://via.placeholder.com/150"
        })

    return productos


def obtener_precios_producto(producto: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    producto_normalizado = producto.lower().strip().replace(" ", "")

    consulta = """
    SELECT p.nombre, t.nombre, pr.precio
    FROM precios pr
    JOIN productos p ON pr.producto_id = p.id_producto
    JOIN tiendas t ON pr.tienda_id = t.id_tienda
    WHERE LOWER(REPLACE(p.nombre, ' ', '')) = %s
    ORDER BY pr.precio ASC
    """

    cursor.execute(consulta, (producto_normalizado,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    productos = []
    for fila in resultado:
        productos.append({
            "nombre": fila[0],
            "tienda": fila[1],
            "precio": float(fila[2]),  
            "imagen": "https://via.placeholder.com/150"  
        })

    return productos

def obtener_historial_precios(producto: str):

    conexion = conectar_base()
    cursor = conexion.cursor()
    producto_normalizado = producto.lower().strip().replace(" ", "")

    consulta = """
    SELECT t.nombre, pr.precio, pr.fecha_actual
    FROM precios pr
    JOIN productos p ON pr.producto_id = p.id_producto
    JOIN tiendas t ON pr.tienda_id = t.id_tienda
    WHERE LOWER(REPLACE(p.nombre, ' ', '')) = %s
    ORDER BY pr.fecha_actual
    """

    cursor.execute(consulta, (producto_normalizado,))
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado


