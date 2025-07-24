from mongoengine import Document, StringField

class ProgramaFormacion(Document):
    """
    Modelo que representa los programas de formación disponibles.
    Se guarda en la colección 'programa_formacion'.
    """
    nombre = StringField(required=True, unique=True)

    meta = {
        'collection': 'programa_formacion',
        'ordering': ['nombre'],
        'strict': False
    }
