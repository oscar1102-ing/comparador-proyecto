from repositories import usuario_repository as repo
from repositories import codigo_repository
from services import email_service
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_cambiala")
ALGORITHM = "HS256"

def registrar_usuario(datos):
    if repo.verificar_email_existe(datos.email):
        return {"error": "El correo ya está registrado"}
    usuario = repo.crear_usuario(datos.nombre, datos.email, datos.password)
    if not usuario:
        return {"error": "Error al crear usuario"}
    return {"mensaje": "Registro exitoso", "usuario": usuario}

def login(datos):
    usuario = repo.obtener_usuario_por_email(datos.email)
    if not usuario:
        return {"error": "Credenciales incorrectas"}
    
    password_hash = usuario[3]
    if not bcrypt.checkpw(datos.password.encode('utf-8'), password_hash.encode('utf-8')):
        return {"error": "Credenciales incorrectas"}
    
    codigo = codigo_repository.generar_codigo(usuario[0])
    enviado = email_service.enviar_codigo(usuario[2], codigo, usuario[1])
    
    if not enviado:
        return {"error": "Error al enviar el código de verificación"}
    
    return {
        "mfa_requerido": True,
        "usuario_id": usuario[0],
        "mensaje": f"Código enviado a {usuario[2]}"
    }

def verificar_mfa(usuario_id: int, codigo: str):
    usuario = repo.obtener_usuario_por_id(usuario_id)
    if not usuario:
        return {"error": "Usuario no encontrado"}
    
    valido = codigo_repository.verificar_codigo(usuario_id, codigo)
    if not valido:
        return {"error": "Código incorrecto o expirado"}
    
    token = jwt.encode({
        "sub": str(usuario[0]),
        "nombre": usuario[1],
        "email": usuario[2],
        "rol": usuario[4] if len(usuario) > 4 else "usuario",  # ← rol en el token
        "exp": datetime.utcnow() + timedelta(days=7)
    }, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "token": token,
        "usuario": {
            "id": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2],
            "rol": usuario[4] if len(usuario) > 4 else "usuario"  # ← rol en la respuesta
        }
    }

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
