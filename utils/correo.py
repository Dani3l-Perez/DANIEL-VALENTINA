import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Cargar las variables del archivo .env
load_dotenv()

def enviar_credenciales(destinatario, nombre, correo, password):
    #Variables de entorno desde el archivo .env
    remitente = os.getenv("MAIL_USER")
    clave = os.getenv("MAIL_PASS")
    servidor_smtp = os.getenv("MAIL_SERVER")
    puerto = int(os.getenv("MAIL_PORT"))

    #Crear el mensaje del correo
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Credenciales de acceso - Sistema de Guías'

    #Cuerpo del mensaje
    cuerpo = f"""
Hola {nombre},

Bienvenido al sistema de guías de aprendizaje.

Tus credenciales de acceso son:

Usuario: {correo}
Contraseña: {password}

Ingresa al sistema para subir tus guías.

Saludos,
Equipo del sistema:
- Valentina Cuaran
- Daniel Pérez
"""
    # Agregar el cuerpo al mensaje
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    #Enviar el correo
    try:
        servidor = smtplib.SMTP(servidor_smtp, puerto)
        servidor.starttls()  # Activar cifrado
        servidor.login(remitente, clave)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()
        print("Correo enviado con éxito a", destinatario)
    except Exception as e:
        print("Error al enviar correo:", e)
