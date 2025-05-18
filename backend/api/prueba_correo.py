import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '..', '..', '.env')

# Carga el archivo .env desde esa ruta
load_dotenv(dotenv_path=env_path)

# 👇 Carga el archivo .env indicando ruta absoluta
EMAIL = os.environ.get('EMAIL_USER')
APP_PASSWORD = os.environ.get('EMAIL_APP_PASS')

print('EMAIL:', EMAIL)
print('APP_PASSWORD:', '*****' if APP_PASSWORD else None)


def enviar_correo(destinatario):
    asunto = 'Gracias por tu compra'
    cuerpo = 'Hola Pepe, gracias por comprar en CardShop. ¡Esperamos que disfrutes tus cartas!'

    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = EMAIL
    msg['To'] = destinatario

    try:
        conexion = smtplib.SMTP('smtp.gmail.com', 587)
        conexion.starttls()
        conexion.login(EMAIL, APP_PASSWORD)
        conexion.sendmail(EMAIL, [destinatario], msg.as_string())
        conexion.quit()
        print(f'✅ Correo enviado correctamente a {destinatario}')
    except Exception as e:
        print(f'❌ Error al enviar el correo: {e}')


# Ejecutar prueba
enviar_correo('davidsamuel.dev2007@gmail.com')
