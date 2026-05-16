import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

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
