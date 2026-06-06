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


def obtener_precios_producto(producto: str, categoria: str = "", pagina: int = 1, 
                              por_pagina: int = 10, tienda: str = "", 
                              precio_min: str = "", precio_max: str = ""):
    conexion = conectar_base()
    cursor = conexion.cursor()

    producto_normalizado = producto.lower().strip().replace(" ", "")
    categoria_normalizada = categoria.lower().strip()

    condiciones = []
    params = []

    # Si no hay búsqueda ni categoría, mostrar todos
    if not producto_normalizado and not categoria_normalizada:
        condiciones.append("1=1")

    # Filtro por texto de búsqueda
    if producto_normalizado:
        condiciones.append("LOWER(REPLACE(p.nombre, ' ', '')) LIKE %s")
        params.append(f"%{producto_normalizado}%")

    # Filtro por categoría (se combina con la búsqueda si hay)
    # Reemplaza el filtro de categoría por esto:
    if categoria_normalizada:
        cats = [c.strip() for c in categoria_normalizada.split(",")]
        placeholders = ", ".join(["%s"] * len(cats))
        condiciones.append(f"LOWER(c.nombre) IN ({placeholders})")
        params.extend(cats)
    # Filtro por tienda (puede venir separado por comas)
    if tienda:
        tiendas_lista = [t.strip() for t in tienda.split(",")]
        placeholders = ", ".join(["%s"] * len(tiendas_lista))
        condiciones.append(f"LOWER(t.nombre) IN ({placeholders})")
        params.extend([t.lower() for t in tiendas_lista])

    # Filtro por precio mínimo
    if precio_min:
        try:
            condiciones.append("pr.precio >= %s")
            params.append(float(precio_min))
        except ValueError:
            pass

    # Filtro por precio máximo
    if precio_max:
        try:
            condiciones.append("pr.precio <= %s")
            params.append(float(precio_max))
        except ValueError:
            pass

    where = """
        FROM precios pr
        JOIN productos p ON pr.producto_id = p.id
        JOIN tiendas t ON pr.tienda_id = t.id
        JOIN categorias c ON p.categoria_id = c.id
        WHERE {condiciones}
    """.format(condiciones=" AND ".join(condiciones))

    cursor.execute(f"SELECT COUNT(*) {where}", params)
    total = cursor.fetchone()[0]

    cursor.execute(f"""
        SELECT p.id, p.nombre, t.nombre, pr.precio, p.imagen_url
        {where}
        ORDER BY pr.precio ASC
        LIMIT %s OFFSET %s
    """, params + [por_pagina, (pagina - 1) * por_pagina])

    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()

    return {
        "productos": [
            {
                "id": fila[0],
                "nombre": fila[1],
                "tienda": fila[2],
                "precio": float(fila[3]),
                "imagen": fila[4] or "imagenes/logo1.png"
            }
            for fila in resultado
        ],
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


