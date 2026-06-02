from database import conectar_base
 
# ============================================
# OBTENER SEDES DE UNA TIENDA
# ============================================
def obtener_sedes_por_tienda(nombre_tienda: str):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            SELECT s.nombre, s.direccion, s.latitud, s.longitud,
                   t.logo_url, t.sitio_web
            FROM sedes s
            JOIN tiendas t ON s.tienda_id = t.id
            WHERE LOWER(t.nombre) LIKE LOWER(%s)
            ORDER BY s.nombre
        """, (f"%{nombre_tienda}%",))
        filas = cursor.fetchall()
        return [
            {
                "nombre": f[0],
                "direccion": f[1],
                "lat": float(f[2]),
                "lon": float(f[3]),
                "logo_url": f[4],
                "sitio_web": f[5]
            }
            for f in filas
        ]
    except Exception as e:
        print(f"Error obteniendo sedes: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# OBTENER SEDES DE VARIAS TIENDAS
# ============================================
def obtener_sedes_por_tiendas(nombres_tiendas: list):
    if not nombres_tiendas:
        return []
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        resultados = []
        for nombre in nombres_tiendas:
            cursor.execute("""
                SELECT s.nombre, s.direccion, s.latitud, s.longitud,
                       t.logo_url, t.sitio_web, t.nombre as tienda_nombre
                FROM sedes s
                JOIN tiendas t ON s.tienda_id = t.id
                WHERE LOWER(t.nombre) LIKE LOWER(%s)
                ORDER BY s.nombre
            """, (f"%{nombre}%",))
            filas = cursor.fetchall()
            for f in filas:
                resultados.append({
                    "nombre": f[0],
                    "direccion": f[1],
                    "lat": float(f[2]),
                    "lon": float(f[3]),
                    "logo_url": f[4],
                    "sitio_web": f[5],
                    "tienda": f[6]
                })
        return resultados
    except Exception as e:
        print(f"Error obteniendo sedes múltiples: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()
 
