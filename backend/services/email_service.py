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


# ============================================
# AGREGAR ESTA FUNCIÓN A TU email_service.py
# ============================================
def enviar_factura_plan(email_destino: str, nombre: str, plan: str, pdf_bytes: bytes):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    import os
    from dotenv import load_dotenv
    load_dotenv()
 
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
 
    nombres_plan = {"basico": "Plan Básico", "pro": "Plan Pro"}
    precios_plan = {"basico": "COP $19.900/mes", "pro": "COP $39.900/mes"}
    nombre_plan = nombres_plan.get(plan, plan)
    precio_plan = precios_plan.get(plan, "")
 
    mensaje = MIMEMultipart("mixed")
    mensaje["Subject"] = f"Solicitud de {nombre_plan} activado - PriceCompare"
    mensaje["From"] = MAIL_FROM
    mensaje["To"] = email_destino
 
    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
        <div style="background: #ff6b00; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">PriceCompare</h1>
        </div>
        <div style="padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px;">
            <h2>Hola, {nombre} 👋</h2>
            <p>Tu <strong>{nombre_plan}</strong> ha sido activado exitosamente. 🎉</p>
 
            <div style="background: #fff8f0; border-left: 4px solid #ff6b00;
                        padding: 16px; border-radius: 0 8px 8px 0; margin: 20px 0;">
                <p style="margin:0; font-size:15px;">
                    <strong>Plan solicitado:</strong> {nombre_plan}<br>
                    <strong>Valor mensual:</strong> {precio_plan}
                </p>
            </div>
 
            <p>Adjuntamos el comprobante de pago en PDF.</p>
            <p>Tu plan ya está activo. Disfruta de todos los beneficios.</p>
 
            <p style="color: #888; font-size: 13px; margin-top: 20px;">
                Si no fuiste tú quien solicitó este plan, ignora este correo.
            </p>
        </div>
    </body></html>
    """
 
    parte_html = MIMEText(html, "html")
    mensaje.attach(parte_html)
 
    # Adjuntar PDF
    adjunto = MIMEApplication(pdf_bytes, _subtype="pdf")
    adjunto.add_header("Content-Disposition", "attachment",
                       filename=f"comprobante_{plan}_pricecompare.pdf")
    mensaje.attach(adjunto)
 
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_FROM, email_destino, mensaje.as_string())
        return True
    except Exception as e:
        print(f"Error enviando factura: {e}")
        return False


def enviar_bienvenida(email_destino: str, nombre: str):
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "¡Bienvenido a PriceCompare! 🎉"
    mensaje["From"] = MAIL_FROM
    mensaje["To"] = email_destino

    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
        <div style="background: #ff6b00; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">PriceCompare</h1>
            <p style="color: white; margin: 6px 0 0; font-size: 14px;">Compara precios, ahorra más</p>
        </div>
        <div style="padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px;">
            <h2>¡Hola, {nombre}! 👋</h2>
            <p>Tu cuenta ha sido creada exitosamente. Ahora puedes comparar precios entre las mejores tiendas de Colombia.</p>

            <!-- Planes -->
            <h3 style="color: #ff6b00; margin-top: 28px;">📦 Nuestros planes</h3>

            <!-- Plan Gratuito -->
            <div style="border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 16px; margin-bottom: 12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:15px;">👤 Plan Gratuito</span>
                    <span style="font-weight:700; color:#64748b;">$0 / mes</span>
                </div>
                <ul style="color:#555; font-size:13px; margin:10px 0 0; padding-left:18px; line-height:1.8;">
                    <li>5 comparaciones por mes</li>
                    <li>5 productos favoritos</li>
                    <li>Historial de búsquedas (10 entradas)</li>
                </ul>
            </div>

            <!-- Plan Básico -->
            <div style="border: 1.5px solid #f59e0b; border-radius: 10px; padding: 16px; margin-bottom: 12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:15px;">⭐ Plan Básico</span>
                    <span style="font-weight:700; color:#f59e0b;">$19.900 / mes</span>
                </div>
                <ul style="color:#555; font-size:13px; margin:10px 0 0; padding-left:18px; line-height:1.8;">
                    <li>20 comparaciones por mes</li>
                    <li>50 productos favoritos</li>
                    <li>Historial ilimitado</li>
                    <li>3 alertas de precio</li>
                </ul>
            </div>

            <!-- Plan Pro -->
            <div style="border: 1.5px solid #0ea5e9; border-radius: 10px; padding: 16px; margin-bottom: 24px; background:#f0f9ff;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:15px;">💎 Plan Pro</span>
                    <span style="font-weight:700; color:#0ea5e9;">$39.900 / mes</span>
                </div>
                <ul style="color:#555; font-size:13px; margin:10px 0 0; padding-left:18px; line-height:1.8;">
                    <li>Comparaciones ilimitadas</li>
                    <li>Favoritos ilimitados</li>
                    <li>Historial ilimitado</li>
                    <li>Alertas ilimitadas</li>
                </ul>
            </div>

            <div style="text-align:center;">
                <a href="http://44.223.85.57/planes.html"
                   style="background:#ff6b00; color:white; padding:12px 28px; border-radius:8px;
                          text-decoration:none; font-size:15px; font-weight:600;">
                    Ver planes →
                </a>
            </div>

            <p style="color:#888; font-size:12px; margin-top:24px; text-align:center;">
                Si no fuiste tú quien se registró, ignora este correo.
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
        print(f"Error enviando bienvenida: {e}")
        return False
        
        
def enviar_cambio_email(email_destino: str, nombre: str):
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Tu correo fue actualizado - PriceCompare"
    mensaje["From"] = MAIL_FROM
    mensaje["To"] = email_destino

    html = f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 520px; margin: auto;">
        <div style="background: #ff6b00; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="color: white; margin: 0;">PriceCompare</h1>
        </div>
        <div style="padding: 30px; border: 1px solid #ddd; border-radius: 0 0 8px 8px;">
            <h2>Hola, {nombre} 👋</h2>
            <p>Tu correo electrónico ha sido actualizado exitosamente en PriceCompare.</p>
            <div style="background: #fff3cd; border-left: 4px solid #ff6b00;
                        padding: 12px 16px; border-radius: 0 8px 8px 0; color: #555;">
                ⚠️ Si no fuiste tú quien hizo este cambio, contáctanos de inmediato.
            </div>
            <p style="color: #888; font-size: 13px; margin-top: 20px;">
                Este correo es solo una notificación, no se requiere ninguna acción.
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
        print(f"Error enviando notificación de cambio de email: {e}")
        return False
