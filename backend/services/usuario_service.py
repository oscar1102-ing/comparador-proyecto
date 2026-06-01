from repositories import usuario_repository as repo
from services import totp_service
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
 
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_cambiala")
ALGORITHM = "HS256"
 
# ============================================
# REGISTRO — genera TOTP y devuelve QR
# ============================================

def registrar_usuario(datos):
    # Limpiar cuentas expiradas
    repo.eliminar_cuentas_expiradas()

    if repo.verificar_email_existe(datos.email):
        return {"error": "El correo ya está registrado"}

    secret = totp_service.generar_secret()
    usuario = repo.crear_usuario(datos.nombre, datos.email, datos.password, secret)
    if not usuario:
        return {"error": "Error al crear usuario"}

    # Generar QR en base64
    qr_base64 = totp_service.generar_qr_base64(secret, datos.email)

    # Enviar correo con el QR
    from services import email_service
    enviado = email_service.enviar_qr_activacion(datos.email, datos.nombre, qr_base64)
    if not enviado:
        # Opcional: loguear error pero no fallar el registro
        print(f"Error enviando correo a {datos.email}")

    # No devolver el QR al frontend
    return {
        "mensaje": "Revisa tu correo electrónico. Te hemos enviado un código QR para activar tu cuenta con Google Authenticator.",
        "usuario_id": usuario[0],
        "expira_en": 240
    }
 
# ============================================
# ACTIVAR MFA — valida código TOTP del QR
# ============================================
def activar_mfa(usuario_id: int, codigo: str):
    usuario = repo.obtener_usuario_por_id(usuario_id)
    if not usuario:
        return {"error": "Usuario no encontrado"}
 
    # usuario[8] = cuenta_pendiente
    if not usuario[8]:
        return {"error": "La cuenta ya fue activada"}
 
    # Verificar que no hayan pasado los 4 minutos desde el registro
    from database import conectar_base
    conexion = conectar_base()
    cursor = conexion.cursor()
    cursor.execute("SELECT fecha_registro FROM usuarios WHERE id = %s", (usuario_id,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
 
    if fila:
        fecha_registro = fila[0]
        # Normalizar timezone para comparar correctamente
        fecha_sin_tz = fecha_registro.replace(tzinfo=None)
        if datetime.utcnow() > fecha_sin_tz + timedelta(minutes=2):
            # Tiempo expirado — eliminar cuenta automáticamente
            repo.eliminar_usuario(usuario_id)
            return {"error": "El tiempo para activar el MFA expiró. Regístrate de nuevo."}
 
    # usuario[6] = totp_secret
    secret = usuario[6]
    if not secret:
        return {"error": "No se encontró la clave TOTP. Regístrate de nuevo."}
 
    if not totp_service.verificar_codigo_totp(secret, codigo):
        return {"error": "Código incorrecto. Intenta de nuevo con Google Authenticator."}
 
    # Activar cuenta
    repo.activar_mfa(usuario_id)
 
    # Generar token JWT para iniciar sesión automáticamente
    token = jwt.encode({
        "sub": str(usuario[0]),
        "nombre": usuario[1],
        "email": usuario[2],
        "rol": usuario[4],
        "exp": datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm=ALGORITHM)
 
    return {
        "token": token,
        "usuario": {
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "rol": usuario[4]
        }
    }
    
    
# Después de la función activar_mfa, agrega:
verificar_mfa = activar_mfa
 
# ============================================
# LOGIN — solo email + password (sin MFA)
# ============================================
def login(datos):
    # Limpiar cuentas expiradas en cada login también
    repo.eliminar_cuentas_expiradas()
 
    usuario = repo.obtener_usuario_por_email(datos.email)
    if not usuario:
        return {"error": "Credenciales incorrectas"}
 
    # Bloquear cuentas que aún no activaron el MFA
    # usuario[8] = cuenta_pendiente
    if usuario[8]:
        return {"error": "Tu cuenta aún no está activada. Completa el registro escaneando el QR."}
 
    password_hash = usuario[3]
    if not bcrypt.checkpw(datos.password.encode('utf-8'), password_hash.encode('utf-8')):
        return {"error": "Credenciales incorrectas"}
 
    # Login exitoso — token directo sin MFA
    token = jwt.encode({
        "sub": str(usuario[0]),
        "nombre": usuario[1],
        "email": usuario[2],
        "rol": usuario[4],
        "exp": datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm=ALGORITHM)
 
    return {
        "token": token,
        "usuario": {
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "rol": usuario[4]
        }
    }
 
# ============================================
# VERIFICAR TOKEN JWT
# ============================================
def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
