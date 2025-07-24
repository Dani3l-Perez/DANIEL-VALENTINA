from flask import Flask
from mongoengine import connect
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conectarse a MongoDB usando la URI
connect(host=os.getenv("MONGO_URI"))

# Definir la carpeta donde se guardarán los PDFs
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'pdfs')

# Importar rutas
from routes.index import *

if __name__ == '__main__':
    app.run(debug=True, port=5400)

