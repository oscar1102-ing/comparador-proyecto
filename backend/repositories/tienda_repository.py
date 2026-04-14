from database import conectar_base

def crear_tienda(nombre: str):

    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    INSERT INTO tiendas(nombre)
    VALUES(%s)
    """

    cursor.execute(consulta,(nombre,))
    conexion.commit()

    cursor.close()
    conexion.close()

    return {"mensaje": "tienda creada"}

def obtener_tienda_nombre(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT id_tienda
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
    JOIN productos p ON pr.producto_id = p.id_producto
    JOIN tiendas t ON pr.tienda_id = t.id_tienda
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