# models/regional.py
from mongoengine import Document, StringField

class Regional(Document):
    nombre = StringField(required=True, unique=True)

    meta = {'collection': 'regionales'}

# utils/poblar_regionales.py
from models.regionales import Regional

regiones = ['Cauca', 'Huila', 'Antioquia', 'Valle', 'Nariño']

for r in regiones:
    if not Regional.objects(nombre=r):
        Regional(nombre=r).save()

print("Regionales insertadas correctamente.")
