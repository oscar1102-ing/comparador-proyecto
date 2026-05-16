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
    SELECT t.nombre, pr.precio
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
            "precio": float(fila[1])
        })

    return tiendas
