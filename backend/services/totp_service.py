import pyotp
import qrcode
import base64
from io import BytesIO
 
APP_NAME = "PriceCompare"
 
# ============================================
# GENERAR CLAVE SECRETA TOTP
# ============================================
def generar_secret():
    return pyotp.random_base32()
 
# ============================================
# GENERAR URL PARA EL QR
# ============================================
def generar_totp_uri(secret: str, email: str):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name=APP_NAME)
 
# ============================================
# GENERAR QR COMO BASE64 (para mostrar en HTML)
# ============================================
def generar_qr_base64(secret: str, email: str):
    uri = generar_totp_uri(secret, email)
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{img_base64}"
 
# ============================================
# VERIFICAR CÓDIGO TOTP
# ============================================
def verificar_codigo_totp(secret: str, codigo: str):
    totp = pyotp.TOTP(secret)
    # valid_window=1 permite 1 intervalo de 30s de margen (tolerancia de reloj)
    return totp.verify(codigo, valid_window=1)
