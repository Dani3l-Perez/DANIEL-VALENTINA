from mongoengine import Document, StringField, ReferenceField, DateTimeField
from datetime import datetime
from models.usuario import Usuario
from models.programa import ProgramaFormacion

class GuiaAprendizaje(Document):
    """
    Modelo que representa una guía de aprendizaje.
    Se guarda en la colección 'guia_aprendizaje'.
    """
    nombre_guia = StringField(required=True, max_length=100)
    descripcion = StringField(required=True, max_length=500)
    programa_formacion = ReferenceField(ProgramaFormacion, required=True)
    archivo_pdf = StringField(required=True)  # Ruta del archivo PDF
    fecha_subida = DateTimeField(default=datetime.now)
    instructor = ReferenceField(Usuario, required=True)  # Usuario que sube la guía

    meta = {
        'collection': 'guia_aprendizaje',
        'ordering': ['-fecha_subida'],
        'strict': False
    }
