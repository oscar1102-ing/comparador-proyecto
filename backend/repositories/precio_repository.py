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
    SELECT 
        p.id,
        p.nombre,
        p.imagen_url,
        t.nombre,
        MIN(pr.precio) as precio_minimo
    FROM productos p
    JOIN precios pr ON pr.producto_id = p.id
    JOIN tiendas t ON pr.tienda_id = t.id
    GROUP BY p.id, p.nombre, p.imagen_url, t.nombre
    ORDER BY precio_minimo ASC
    LIMIT 10
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    productos = []

    for fila in resultado:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "imagen": fila[2],
            "tienda": fila[3],
            "precio": float(fila[4])
        })

    return productos


def obtener_precios_producto(producto: str, categoria: str = "", pagina: int = 1, por_pagina: int = 10):
    conexion = conectar_base()
    cursor = conexion.cursor()
    producto_normalizado = producto.lower().strip().replace(" ", "")
    categoria_normalizada = categoria.lower().strip()

    if categoria_normalizada:
        where = """
            FROM precios pr
            JOIN productos p ON pr.producto_id = p.id
            JOIN tiendas t ON pr.tienda_id = t.id
            JOIN categorias c ON p.categoria_id = c.id
            WHERE LOWER(c.nombre) LIKE %s
        """
        params_count = (f"%{categoria_normalizada}%",)
        params_query = (f"%{categoria_normalizada}%", por_pagina, (pagina - 1) * por_pagina)
    else:
        where = """
            FROM precios pr
            JOIN productos p ON pr.producto_id = p.id
            JOIN tiendas t ON pr.tienda_id = t.id
            WHERE LOWER(REPLACE(p.nombre, ' ', '')) LIKE %s
        """
        params_count = (f"%{producto_normalizado}%",)
        params_query = (f"%{producto_normalizado}%", por_pagina, (pagina - 1) * por_pagina)

    cursor.execute(f"SELECT COUNT(*) {where}", params_count)
    total = cursor.fetchone()[0]

    cursor.execute(f"""
        SELECT p.id, p.nombre, t.nombre, pr.precio, p.imagen_url
        {where}
        ORDER BY pr.precio ASC
        LIMIT %s OFFSET %s
    """, params_query)

    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()

    productos = []
    for fila in resultado:
        productos.append({
            "id": fila[0],
            "nombre": fila[1],
            "tienda": fila[2],
            "precio": float(fila[3]),
            "imagen": fila[4] or "imagenes/logo1.png"
        })

    return {
        "productos": productos,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": -(-total // por_pagina)
    }

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


