import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
 
load_dotenv()
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
 
# ============================================
# ENVIAR QR DE GOOGLE AUTHENTICATOR
# ============================================
def enviar_qr_activacion(email_destino: str, nombre: str, qr_base64: str):
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Activa tu cuenta - PriceCompare"
    mensaje["From"] = MAIL_FROM
    mensaje["To"] = email_destino
 
    # qr_base64 ya viene con el prefijo "data:image/png;base64,..."
    # Para el correo necesitamos solo los datos sin el prefijo
    qr_datos = qr_base64.replace("data:image/png;base64,", "")
 
    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
        <div style="background: #ff6b00; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">PriceCompare</h1>
        </div>
        <div style="padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px;">
            <h2>Hola, {nombre} 👋</h2>
            <p>Tu cuenta fue creada exitosamente. Para activarla necesitas configurar 
               <strong>Google Authenticator</strong>:</p>
 
            <ol style="line-height: 2; color: #444;">
                <li>Descarga <strong>Google Authenticator</strong> en tu celular.</li>
                <li>Abre la app y toca el botón <strong>"+"</strong>.</li>
                <li>Selecciona <em>Escanear código QR</em>.</li>
                <li>Apunta la cámara al código de abajo.</li>
                <li>Ingresa el código de <strong>6 dígitos</strong> que aparece en la app.</li>
            </ol>
 
            <div style="text-align: center; margin: 25px 0;">
                <img src="cid:qr_image" alt="Código QR" 
                     style="border: 3px solid #ff6b00; border-radius: 8px; padding: 8px; background: white;"
                     width="200" height="200">
            </div>
            

 
            <div style="background: #fff3cd; border-left: 4px solid #ff6b00; 
                        padding: 12px 16px; border-radius: 0 8px 8px 0; color: #555;">
                ⏰ <strong>Tienes 2 minutos</strong> para escanear el QR y activar tu cuenta.<br>
                Si no lo haces en ese tiempo, tu cuenta será eliminada y deberás registrarte de nuevo.
            </div>
 
            <p style="color: #888; margin-top: 20px; font-size: 13px;">
                Si no fuiste tú quien se registró, ignora este correo.
            </p>
        </div>
    </body></html>
    """
 
    # Adjuntar el QR como imagen embebida (cid:qr_image)
    from email.mime.image import MIMEImage
    import base64
 
    msg_html = MIMEText(html, "html")
    mensaje.attach(msg_html)
 
    qr_bytes = base64.b64decode(qr_datos)
    img = MIMEImage(qr_bytes, _subtype="png")
    img.add_header("Content-ID", "<qr_image>")
    img.add_header("Content-Disposition", "inline", filename="qr_autenticador.png")
    mensaje.attach(img)
 
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, email_destino, mensaje.as_string())
        return True
    except Exception as e:
        print(f"Error enviando QR por correo: {e}")
        return False
 
 
# ============================================
# ENVIAR CÓDIGO DE VERIFICACIÓN (se mantiene
# por si se usa en otra parte del proyecto)
# ============================================
def enviar_codigo(email_destino: str, codigo: str, nombre: str):
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Tu código de verificación - PriceCompare"
    mensaje["From"] = MAIL_FROM
    mensaje["To"] = email_destino
 
    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 500px; margin: auto;">
        <div style="background: #ff6b00; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">PriceCompare</h1>
        </div>
        <div style="padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px;">
            <h2>Hola, {nombre} 👋</h2>
            <p>Tu código de verificación es:</p>
            <div style="background: #f5f5f5; padding: 20px; text-align: center; 
                        border-radius: 8px; font-size: 36px; font-weight: bold; 
                        letter-spacing: 8px; color: #ff6b00;">
                {codigo}
            </div>
            <p style="color: #888; margin-top: 20px;">
                Este código expira en <strong>5 minutos</strong>.<br>
                Si no fuiste tú, ignora este correo.
            </p>
        </div>
    </body></html>
    """
    mensaje.attach(MIMEText(html, "html"))
 
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, email_destino, mensaje.as_string())
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False

