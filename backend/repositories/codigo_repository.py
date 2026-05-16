from database import conectar_base
from datetime import datetime, timedelta
import random

def generar_codigo(usuario_id: int):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    codigo = str(random.randint(100000, 999999))
    
    cursor.execute("""
        UPDATE codigos_verificacion 
        SET usado = TRUE 
        WHERE usuario_id = %s AND usado = FALSE
    """, (usuario_id,))
    
    # Dejar que PostgreSQL maneje la hora
    cursor.execute("""
        INSERT INTO codigos_verificacion (usuario_id, codigo, expiracion, usado)
        VALUES (%s, %s, NOW() + INTERVAL '5 minutes', FALSE)
    """, (usuario_id, codigo))
    
    conexion.commit()
    cursor.close()
    conexion.close()
    return codigo

def verificar_codigo(usuario_id: int, codigo: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    
    # Debug temporal
    print(f"DEBUG — usuario_id recibido: {usuario_id}, tipo: {type(usuario_id)}")
    
    cursor.execute("""
        SELECT id, codigo, expiracion, usado FROM codigos_verificacion
        WHERE usuario_id = %s
        ORDER BY id DESC LIMIT 1
    """, (usuario_id,))
    debug = cursor.fetchone()
    print(f"DEBUG — BD tiene: {debug}, recibido: '{codigo}'")
    
    cursor.execute("""
        SELECT id FROM codigos_verificacion
        WHERE usuario_id = %s 
        AND codigo = %s 
        AND usado = FALSE 
        AND expiracion > NOW()
    """, (usuario_id, codigo))
    
    resultado = cursor.fetchone()
    print(f"DEBUG — resultado consulta: {resultado}")
    
    if resultado:
        cursor.execute("""
            UPDATE codigos_verificacion SET usado = TRUE WHERE id = %s
        """, (resultado[0],))
        conexion.commit()
    
    cursor.close()
    conexion.close()
    return resultado is not None
