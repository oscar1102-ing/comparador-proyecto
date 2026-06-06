from database import conectar_base

def crear_tienda(datos):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO tiendas(nombre, sitio_web)
        VALUES(%s, %s)
        RETURNING id, nombre
    """, (datos.nombre, datos.url))
    tienda = cursor.fetchone()
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Tienda creada", "id": tienda[0], "nombre": tienda[1]}

def obtener_tienda_nombre(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT id
    FROM tiendas
    WHERE nombre = %s
    """

    cursor.execute(consulta,(nombre,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado

def obtener_todas_tiendas():

    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT *
    FROM tiendas
    """

    cursor.execute(consulta)
    resultado = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultado


def obtener_tiendas_producto(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    consulta = """
    SELECT t.nombre, pr.precio, pr.url_producto
    FROM precios pr
    JOIN productos p ON pr.producto_id = p.id
    JOIN tiendas t ON pr.tienda_id = t.id
    WHERE LOWER(REPLACE(p.nombre, ' ', '')) = %s
    ORDER BY pr.precio ASC
    """
    nombre_normalizado = nombre.lower().strip().replace(" ", "")
    cursor.execute(consulta, (nombre_normalizado,))
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    tiendas = []
    for fila in resultado:
        tiendas.append({
            "tienda": fila[0],
            "precio": float(fila[1]),
            "url": fila[2] or ""
        })
    return tiendas
    
def obtener_tiendas_por_id(producto_id: int):
    import re
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT nombre FROM productos WHERE id = %s", (producto_id,))
        fila = cursor.fetchone()
        if not fila:
            return []
        nombre_base = fila[0]

        # Extraer capacidad en GB
        capacidad_num = None
        match_cap = re.search(r'(\d+)\s*GB', nombre_base, re.IGNORECASE)
        if match_cap:
            capacidad_num = match_cap.group(1)

        # Limpiar nombre para extraer modelo base
        nombre_limpio = nombre_base.lower()
        palabras_eliminar = [
            'celular', 'smartphone', 'teléfono', 'telefono',
            'negro', 'morado', 'verde', 'azul', 'rojo', 'blanco', 'gris',
            '4g', '5g', 'lte', 'reloj', 'inteligente', 'con', 'de', 'los', 'las',
            'ram', 'gb'
        ]
        for p in palabras_eliminar:
            nombre_limpio = nombre_limpio.replace(p, ' ')
        nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio).strip()
        palabras = nombre_limpio.split()
        modelo_base = ' '.join(palabras[:3]) if palabras else nombre_base.lower()

        # Construir condiciones
        condiciones = []
        params = []
        if modelo_base:
            condiciones.append("p.nombre ILIKE %s")
            params.append(f"%{modelo_base}%")
        if capacidad_num:
            condiciones.append("(p.nombre ILIKE %s OR p.nombre ILIKE %s)")
            params.append(f"%{capacidad_num}GB%")
            params.append(f"%{capacidad_num} GB%")

        if not condiciones:
            return []

        where_clause = " AND ".join(condiciones)
        consulta = f"""
        SELECT t.nombre AS tienda,
               MIN(pr.precio) AS precio,
               (ARRAY_AGG(pr.url_producto ORDER BY pr.precio ASC))[1] AS url
        FROM productos p
        JOIN precios pr ON pr.producto_id = p.id
        JOIN tiendas t  ON pr.tienda_id   = t.id
        WHERE {where_clause}
        GROUP BY t.nombre
        ORDER BY precio ASC
        """
        cursor.execute(consulta, params)
        return [
            {"tienda": r[0], "precio": float(r[1]), "url": r[2] or ""}
            for r in cursor.fetchall()
        ]
    except Exception as e:
        print(f"[ERROR] obtener_tiendas_por_id: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        cursor.close()
        conexion.close()
