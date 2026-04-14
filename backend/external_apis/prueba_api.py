# prueba_api_v3.py
import requests
from fake_useragent import UserAgent
import random
import time

print("🔌 Probando con User-Agent rotatorio...")

# Lista de User-Agents reales (por si fake_useragent no funciona)
ua_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
]

# Rotamos User-Agent
headers = {
    "User-Agent": random.choice(ua_list),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

print("📡 Headers enviados:")
for key, value in headers.items():
    print(f"   {key}: {value}")

# Intentamos con diferentes endpoints
endpoints = [
    "https://api.mercadolibre.com/sites/MLA/search?q=iphone+16&limit=1",
    "https://api.mercadolibre.com/sites/MLA/search?q=celular&limit=1", 
    "https://api.mercadolibre.com/items/MLA123456789"  # Producto de ejemplo
]

for i, url in enumerate(endpoints):
    print(f"\n🔄 Intento {i+1} - URL: {url}")
    
    try:
        respuesta = requests.get(url, headers=headers, timeout=10)
        print(f"📡 Código: {respuesta.status_code}")
        
        if respuesta.status_code == 200:
            print("✅ ¡ÉXITO!")
            datos = respuesta.json()
            if 'results' in datos:
                print(f"📦 Resultados: {len(datos['results'])}")
            print(datos)
            break
        else:
            print(f"❌ Error: {respuesta.text[:200]}")
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
    
    time.sleep(2)  # Esperamos 2 segundos entre intentos