from flask import render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from models.usuario import Usuario
from models.programa import ProgramaFormacion
from models.guia import GuiaAprendizaje
from mongoengine.errors import NotUniqueError, DoesNotExist
from utils.correo import enviar_credenciales
from datetime import datetime
import os
from app import app

ALLOWED_EXTENSIONS = {'pdf'}

def archivo_valido(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    regionales = ["Cauca", "Huila", "Antioquia", "Valle", "Nariño"]

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        regional = request.form['regional']

        nombre_formateado = nombre.strip().replace(" ", "").lower()
        regional_formateado = regional.strip().replace(" ", "").lower()

        total_usuarios = Usuario.objects.count()
        numero = total_usuarios + 1

        password = f"{nombre_formateado}{regional_formateado}!{numero}"

        try:
            nuevo_usuario = Usuario(
                nombre_completo=nombre,
                correo=correo,
                regional=regional,
                password=password
            )
            nuevo_usuario.save()

            enviar_credenciales(destinatario=correo, nombre=nombre, correo=correo, password=password)

            return f"Usuario registrado correctamente. Se enviaron las credenciales a: {correo}"

        except NotUniqueError:
            return "El correo ya está registrado", 400

    return render_template('login.html', modo='registrar', regionales=regionales)

@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']

        try:
            usuario = Usuario.objects.get(correo=correo)
            if usuario.password == password:
                session['usuario_id'] = str(usuario.id)
                session['nombre'] = usuario.nombre_completo
                return redirect(url_for('subir_guia'))
            else:
                return "Contraseña incorrecta", 401

        except DoesNotExist:
            return "Usuario no encontrado", 404

    return render_template('login.html', modo='iniciar')

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('iniciarSesion'))

@app.route('/subir_guia', methods=['GET', 'POST'])
def subir_guia():
    if 'usuario_id' not in session:
        return redirect(url_for('iniciarSesion'))

    programas = ProgramaFormacion.objects()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        id_programa = request.form['programa']
        archivo = request.files['archivo']

        if archivo and archivo_valido(archivo.filename):
            nombre_archivo = secure_filename(archivo.filename)
            ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
            archivo.save(ruta_archivo)

            usuario = Usuario.objects.get(id=session['usuario_id'])
            programa = ProgramaFormacion.objects.get(id=id_programa)

            guia = GuiaAprendizaje(
                nombre_guia=nombre,
                descripcion=descripcion,
                archivo_pdf=nombre_archivo,  # Solo el nombre
                programa_formacion=programa,
                instructor=usuario,
                fecha_subida=datetime.now()
            )
            guia.save()

            return redirect(url_for('listar_guias'))

        return "Archivo no válido. Debe ser un PDF.", 400

    return render_template('subir_guia.html', programas=programas)

@app.route('/listar_guias')
def listar_guias():
    if 'usuario_id' not in session:
        return redirect(url_for('iniciarSesion'))

    guias = GuiaAprendizaje.objects().order_by('-fecha_subida')
    return render_template('listar_guias.html', guias=guias)

@app.route('/ver_pdf/<nombre_archivo>')
def ver_pdf(nombre_archivo):
    if 'usuario_id' not in session:
        return redirect(url_for('iniciarSesion'))

    ruta = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
    if os.path.exists(ruta):
        return send_file(ruta, mimetype='application/pdf')
    return "Archivo no encontrado", 404
