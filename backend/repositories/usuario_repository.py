from database import conectar_base
import bcrypt

def crear_usuario(nombre: str, email: str, password: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    import bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    consulta = """
    INSERT INTO usuarios (nombre, email, password)
    VALUES (%s, %s, %s)
    RETURNING id, nombre, email, fecha_registro
    """

    cursor.execute(consulta, (nombre, email, hashed.decode()))
    usuario = cursor.fetchone()

    conexion.commit()
    cursor.close()
    conexion.close()

    return usuario

def verificar_email_existe(email: str):
    conexion = conectar_base()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    existe = cursor.fetchone()

    cursor.close()
    conexion.close()

    return existe is not None


def obtener_usuario_por_email(email: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, email, password, rol FROM usuarios WHERE email = %s",
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def obtener_usuario_por_id(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, email, password, rol FROM usuarios WHERE id = %s",
        (id,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario
