from database import conectar_base

def crear_producto(nombre: str, categoria: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    INSERT INTO productos(nombre, categoria)
    VALUES(%s,%s)
    """

    cursor.execute(consulta,(nombre,categoria))

    conexion.commit()


    cursor.close()
    conexion.close()

    return {"mensaje" : "producto agregado"}


def obtener_producto_id(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()

    consulta = """
    SELECT id_producto
    FROM productos
    WHERE id_producto = %s
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
    SELECT nombre
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
        "nombre": fila[0],
        "imagen": "https://via.placeholder.com/200"
    }


def obtener_similares(nombre: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    palabra = nombre.split(" ")[0].lower()

    consulta = """
    SELECT p.nombre, MIN(pr.precio) as precio
    FROM productos p
    JOIN precios pr ON pr.producto_id = p.id_producto
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