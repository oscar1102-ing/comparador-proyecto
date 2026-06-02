from database import conectar_base
import bcrypt

# ============================================
# CREAR USUARIO (con TOTP secret, cuenta pendiente)
# ============================================
def crear_usuario(nombre: str, email: str, password: str, totp_secret: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    consulta = """
    INSERT INTO usuarios (nombre, email, password, rol, totp_secret, mfa_activado, cuenta_pendiente)
    VALUES (%s, %s, %s, 'usuario', %s, FALSE, TRUE)
    RETURNING id, nombre, email, fecha_registro
    """
    cursor.execute(consulta, (nombre, email, hashed.decode(), totp_secret))
    usuario = cursor.fetchone()
    conexion.commit()
    cursor.close()
    conexion.close()
    return usuario


# ============================================
# VERIFICAR SI EMAIL YA EXISTE
# ============================================
def verificar_email_existe(email: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    existe = cursor.fetchone()
    cursor.close()
    conexion.close()
    return existe is not None



# ============================================
# OBTENER USUARIO POR EMAIL
# Índices: 0=id, 1=nombre, 2=email, 3=password,
#          4=rol, 5=es_root, 6=totp_secret,
#          7=mfa_activado, 8=cuenta_pendiente
# ============================================
def obtener_usuario_por_email(email: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT id, nombre, email, password, rol, es_root,
                  totp_secret, mfa_activado, cuenta_pendiente
           FROM usuarios WHERE email = %s""",
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario


# ============================================
# OBTENER USUARIO POR ID
# Índices: 0=id, 1=nombre, 2=email, 3=password,
#          4=rol, 5=es_root, 6=totp_secret,
#          7=mfa_activado, 8=cuenta_pendiente
# ============================================
def obtener_usuario_por_id(id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT id, nombre, email, password, rol, es_root,
                  totp_secret, mfa_activado, cuenta_pendiente
           FROM usuarios WHERE id = %s""",
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
        "SELECT id, nombre, email, rol, es_root, mfa_activado, fecha_registro FROM usuarios ORDER BY id"
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
            "mfa_activado": f[5],
            "fecha_registro": str(f[6])
        }
        for f in filas
    ]

 
# ============================================
# ELIMINAR USUARIO (protegido: no elimina root)
# ============================================
def eliminar_usuario(id: int):
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
        return {"error": "No se puede eliminar al superusuario root"}
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": "Usuario eliminado correctamente"}
 

 
# ============================================
# CAMBIAR ROL (protegido: no modifica root)
# ============================================
def cambiar_rol(id: int, nuevo_rol: str):
    roles_validos = ['usuario', 'basico', 'pro', 'admin', 'root']
    if nuevo_rol not in roles_validos:
        return {"error": f"Rol inválido. Opciones: {', '.join(roles_validos)}"}
 
    from database import conectar_base
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
    cursor.execute("UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, id))
    conexion.commit()
    cursor.close()
    conexion.close()
    return {"mensaje": f"Rol actualizado a {nuevo_rol}"}


# ============================================
# ACTIVAR MFA (marcar cuenta como activa)
# ============================================
def activar_mfa(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET mfa_activado = TRUE,
            cuenta_pendiente = FALSE,
            mfa_activado_en = NOW()
        WHERE id = %s
    """, (usuario_id,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
# ============================================
# ELIMINAR CUENTAS PENDIENTES EXPIRADAS
# Cuentas que no activaron MFA en 4 minutos
# ============================================
def eliminar_cuentas_expiradas():
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("""
        DELETE FROM usuarios
        WHERE cuenta_pendiente = TRUE
        AND fecha_registro < NOW() - INTERVAL '2 minutes'
        AND (es_root IS NULL OR es_root = FALSE)
    """)
    eliminados = cursor.rowcount
    conexion.commit()
    cursor.close()
    conexion.close()
    return eliminados
