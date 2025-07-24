from mongoengine import Document, StringField, EmailField
from mongoengine.errors import ValidationError

class Usuario(Document):
    """
    Modelo para representar un instructor registrado en el sistema.
    Se guarda en la colección 'usuario'.
    """
    nombre_completo = StringField(required=True, max_length=100)
    correo = EmailField(required=True, unique=True)
    regional = StringField(required=True, choices=[
        'Cauca', 'Huila', 'Antioquia', 'Valle', 'Nariño'
    ])
    password = StringField(required=True, min_length=6)

    meta = {
        'collection': 'usuario',  # Nombre personalizado para la colección
        'ordering': ['nombre_completo'],
        'strict': False
    }

    def clean(self):
        # Validaciones personalizadas si las necesitas
        if not self.regional:
            raise ValidationError("La regional es obligatoria")
