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
    
# ============================================
# LISTAR TODOS LOS USUARIOS
# ============================================
def listar_usuarios():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id, nombre, email, rol, es_root, fecha_registro FROM usuarios ORDER BY id"
    )
    filas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return [
        {
            "id": f[0],
            "nombre": f[1],
            "email": f[2],
            "rol": f[3],
            "es_root": f[4],
            "fecha_registro": str(f[5])
        }
        for f in filas
    ]
 
# ============================================
# ELIMINAR USUARIO (protegido: no elimina root)
# ============================================
def eliminar_usuario(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
 
    # Verificar que no sea root
    cursor.execute("SELECT es_root, rol FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()
 
    if not usuario:
        cursor.close()
        conexion.close()
        return {"error": "Usuario no encontrado"}
 
    if usuario[0] is True or usuario[1] == 'root':
        cursor.close()
        conexion.close()
        return {"error": "No se puede eliminar al superusuario root"}
 
    # Eliminar registros relacionados primero
    cursor.execute("DELETE FROM codigos_verificacion WHERE usuario_id = %s", (id,))
    cursor.execute("DELETE FROM favoritos WHERE usuario_id = %s", (id,))
    cursor.execute("DELETE FROM historial_busquedas WHERE usuario_id = %s", (id,))
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Usuario eliminado correctamente"}
 
# ============================================
# CAMBIAR ROL (protegido: no modifica root)
# ============================================
def cambiar_rol(id: int, nuevo_rol: str):
    roles_validos = ['usuario', 'premium', 'admin', 'root']
    
    if nuevo_rol not in roles_validos:
        return {"error": f"Rol inválido. Opciones: {', '.join(roles_validos)}"}

    conexion = conectar_base()
    cursor = conexion.cursor()

    cursor.execute("SELECT es_root, rol FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexion.close()
        return {"error": "Usuario no encontrado"}

    if usuario[0] is True or usuario[1] == 'root':
        cursor.close()
        conexion.close()
        return {"error": "No se puede modificar el rol del superusuario root"}

    if nuevo_rol == 'root':
        cursor.execute(
            "UPDATE usuarios SET rol = %s, es_root = TRUE WHERE id = %s",
            (nuevo_rol, id)
        )
    else:
        cursor.execute(
            "UPDATE usuarios SET rol = %s, es_root = FALSE WHERE id = %s",
            (nuevo_rol, id)
        )

    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": f"Rol actualizado a {nuevo_rol}"}
