import requests
import time
from database import conectar_base
 
SERVIDORES_OVERPASS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]
 
# ============================================
# BUSCAR SEDES EN OPENSTREETMAP
# ============================================
def obtener_sedes_osm(nombre_marca, ciudad="Bogotá"):
    print(f"\n🌍 Buscando sedes de '{nombre_marca}' en {ciudad}...")
 
    query = f"""
    [out:json][timeout:90];
    area["name"="{ciudad}"]->.searchArea;
    (
      node["brand"="{nombre_marca}"]["shop"="supermarket"](area.searchArea);
      way["brand"="{nombre_marca}"]["shop"="supermarket"](area.searchArea);
      node["brand"="{nombre_marca}"]["shop"="department_store"](area.searchArea);
      way["brand"="{nombre_marca}"]["shop"="department_store"](area.searchArea);
      node["name"="{nombre_marca}"]["shop"="supermarket"](area.searchArea);
      way["name"="{nombre_marca}"]["shop"="supermarket"](area.searchArea);
    );
    out center;
    """
 
    headers = {"User-Agent": "MapaSedes/1.0"}
 
    for servidor in SERVIDORES_OVERPASS:
        print(f"  🔄 Intentando: {servidor}")
        try:
            response = requests.post(
                servidor,
                data={"data": query},
                headers=headers,
                timeout=90
            )
            if response.status_code == 200 and response.text.strip():
                data = response.json()
                print("  ✅ Datos recibidos")
                break
        except Exception as e:
            print(f"  ❌ Error: {e}")
    else:
        return []
 
    sedes = []
    elementos = data.get("elements", [])
    print(f"  📍 Elementos en OSM: {len(elementos)}")
 
    for element in elementos:
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
 
        tags = element.get("tags", {})
        sucursal = tags.get("branch")
        nombre = f"{nombre_marca} {sucursal}" if sucursal else tags.get("name", nombre_marca)
        direccion = (
            f"{tags.get('addr:street', '')} {tags.get('addr:housenumber', '')}".strip()
            or tags.get("addr:full")
            or "Ubicación en mapa"
        )
        sedes.append({"nombre": nombre, "lat": lat, "lon": lon, "dir": direccion})
 
    # Eliminar duplicados
    sedes_unicas = []
    vistos = set()
    for sede in sedes:
        clave = (sede["nombre"], round(float(sede["lat"]), 5), round(float(sede["lon"]), 5))
        if clave not in vistos:
            vistos.add(clave)
            sedes_unicas.append(sede)
 
    return sedes_unicas
 
# ============================================
# EXTRAER DIRECCIÓN CORTA
# ============================================
def extraer_direccion_corta(direccion):
    if not direccion:
        return "Sede Bogotá"
    palabras = direccion.strip().split()
    claves = ["calle", "carrera", "avenida", "av", "diag", "transversal", "tv"]
    for i, palabra in enumerate(palabras):
        if palabra.lower() in claves:
            resultado = [palabra]
            if i + 1 < len(palabras):
                resultado.append(palabras[i + 1])
            return " ".join(resultado)
    return "Sede Bogotá"
 
# ============================================
# POBLAR SEDES — usa tabla tiendas existente
# ============================================
def poblar_sedes_tienda(nombre_tienda: str, logo_url: str = None, sitio_web: str = None):
    conexion = conectar_base()
    cursor = conexion.cursor()
    try:
        print(f"\n{'='*45}")
        print(f"🚀 PROCESANDO: {nombre_tienda}")
        print(f"{'='*45}")
 
        # Obtener o crear tienda en la tabla tiendas
        cursor.execute("SELECT id FROM tiendas WHERE LOWER(nombre) = LOWER(%s)", (nombre_tienda,))
        fila = cursor.fetchone()
 
        if fila:
            tienda_id = fila[0]
            # Actualizar logo y sitio_web si se pasan
            if logo_url or sitio_web:
                cursor.execute("""
                    UPDATE tiendas
                    SET logo_url = COALESCE(%s, logo_url),
                        sitio_web = COALESCE(%s, sitio_web)
                    WHERE id = %s
                """, (logo_url, sitio_web, tienda_id))
            print(f"  ✅ Tienda ya existe (id={tienda_id})")
        else:
            cursor.execute("""
                INSERT INTO tiendas (nombre, sitio_web, logo_url)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (nombre_tienda, sitio_web, logo_url))
            tienda_id = cursor.fetchone()[0]
            print(f"  ✅ Tienda creada (id={tienda_id})")
 
        # Buscar sedes en OSM
        sedes = obtener_sedes_osm(nombre_tienda)
 
        if not sedes:
            print(f"  ⚠️  No se encontraron sedes físicas para {nombre_tienda}")
            conexion.commit()
            return 0
 
        contador = 0
        for sede in sedes:
            direccion_corta = extraer_direccion_corta(sede["dir"])
            nombre_unico = f"{sede['nombre']} - {direccion_corta}"
 
            cursor.execute("""
                INSERT INTO sedes (tienda_id, nombre, direccion, latitud, longitud)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nombre, tienda_id) DO NOTHING
            """, (tienda_id, nombre_unico, sede["dir"], sede["lat"], sede["lon"]))
            contador += 1
 
        conexion.commit()
        print(f"  ✅ {contador} sedes guardadas para {nombre_tienda}")
        return contador
 
    except Exception as e:
        conexion.rollback()
        print(f"  ❌ ERROR: {e}")
        return 0
    finally:
        cursor.close()
        conexion.close()
 
# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    inicio = time.time()
 
    # Agrega aquí las tiendas que quieres poblar
    TIENDAS = [
        {
            "nombre": "Éxito",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Logo_%C3%89xito.svg/512px-Logo_%C3%89xito.svg.png",
            "sitio_web": "https://www.exito.com/"
        },
        {
            "nombre": "Falabella",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Falabella_logo.svg/512px-Falabella_logo.svg.png",
            "sitio_web": "https://www.falabella.com.co/"
        },
        {
            "nombre": "Mercado Libre",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Mercado_Libre_logo.svg/512px-Mercado_Libre_logo.svg.png",
            "sitio_web": "https://www.mercadolibre.com.co/"
        },
        {
            "nombre": "Alkosto",
            "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Alkosto_logo.svg/512px-Alkosto_logo.svg.png",
            "sitio_web": "https://www.alkosto.com/"
        }
    ]
 
    total = 0
    for tienda in TIENDAS:
        total += poblar_sedes_tienda(
            nombre_tienda=tienda["nombre"],
            logo_url=tienda["logo"],
            sitio_web=tienda["sitio_web"]
        )
        time.sleep(3)  # pausa entre tiendas para no saturar OSM
 
    fin = time.time()
    print(f"\n{'='*45}")
    print(f"✅ TOTAL SEDES GUARDADAS: {total}")
    print(f"⏱  Tiempo: {round(fin - inicio, 2)}s")
    print(f"{'='*45}")
 
