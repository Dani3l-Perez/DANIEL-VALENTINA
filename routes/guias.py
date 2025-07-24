# from flask import render_template, request, redirect, url_for, session,send_file
# from werkzeug.utils import secure_filename
# import os
# from datetime import datetime

# from models.guia import GuiaAprendizaje
# from models.programa import ProgramaFormacion
# from models.usuario import Usuario
# from app import app

# # Carpeta donde se guardarán los PDFs
# UPLOAD_FOLDER = os.path.join('static', 'pdfs')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Extensiones permitidas
# ALLOWED_EXTENSIONS = {'pdf'}

# def archivo_valido(nombre):
#     return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # =============================================================
# # RUTA PARA SUBIR UNA GUÍA DE APRENDIZAJE
# # =============================================================
# @app.route('/subir_guia', methods=['GET', 'POST'])
# def subir_guia():
#     """
#     Permite a un instructor subir una guía en formato PDF con sus detalles.
#     - GET: muestra el formulario.
#     - POST: guarda la guía y el archivo.
#     """
#     if 'usuario_id' not in session:
#         return redirect(url_for('iniciarSesion'))

#     programas = ProgramaFormacion.objects()

#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         descripcion = request.form['descripcion']
#         id_programa = request.form['programa']
#         archivo = request.files['archivo']

#         if archivo and archivo_valido(archivo.filename):
#             nombre_archivo = secure_filename(archivo.filename)
#             ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_archivo)
#             archivo.save(ruta_archivo)

#             # Datos de sesión
#             usuario = Usuario.objects.get(id=session['usuario_id'])
#             programa = ProgramaFormacion.objects.get(id=id_programa)

#             guia = GuiaAprendizaje(
#                 nombre_guia=nombre,
#                 descripcion=descripcion,
#                 archivo_pdf=ruta_archivo,
#                 programa_formacion=programa,
#                 instructor=usuario,
#                 fecha_subida=datetime.now()
#             )
#             guia.save()

#             return redirect(url_for('listar_guias'))

#         return "Archivo no válido. Debe ser un PDF.", 400

#     return render_template('subir_guia.html', programas=programas)

# # =============================================================
# # RUTA PARA LISTAR GUÍAS DE APRENDIZAJE
# # =============================================================
# @app.route('/listar_guias')
# def listar_guias():
#     """
#     Muestra todas las guías de aprendizaje en una tabla.
#     """
#     if 'usuario_id' not in session:
#         return redirect(url_for('iniciarSesion'))

#     guias = GuiaAprendizaje.objects().order_by('-fecha_subida')
#     return render_template('listar_guias.html', guias=guias)

# # =============================================================
# # RUTA PARA VER UN PDF
# # =============================================================
# @app.route('/ver_pdf/<path:ruta>')
# def ver_pdf(ruta):
#     """
#     Muestra el PDF al hacer clic en el icono.
#     """
#     return send_file(f"static/pdfs/{ruta}", mimetype='application/pdf')
# from flask import render_template, request, redirect, url_for, session
# from models.usuario import Usuario  # Modelo de usuario con mongoengine
# from models.regionales import Regional  # NUEVO: Modelo de regionales
# from mongoengine.errors import NotUniqueError, DoesNotExist
# from utils.correo import enviar_credenciales  # Función para enviar correos
# from app import app
# from routes import guias

# # =============================================================
# # RUTA PRINCIPAL
# # =============================================================
# @app.route('/')
# def index():
#     """
#     Página principal. Muestra el menú con enlaces a iniciar sesión o registrarse.
#     """
#     return render_template('index.html')


# # =============================================================
# # RUTA PARA REGISTRARSE
# # =============================================================
# @app.route('/registrarse', methods=['GET', 'POST'])
# def registrarse():
#     """
#     Permite registrar un usuario instructor.
#     - GET: muestra el formulario de registro.
#     - POST: guarda el usuario y envía credenciales por correo.
#     """
#     # Consulta las regionales desde la base de datos
#     regionales = [r.nombre for r in Regional.objects()]

#     if request.method == 'POST':
#         nombre = request.form['nombre']
#         correo = request.form['correo']
#         regional = request.form['regional']

#         # Formatear para crear una contraseña sencilla
#         nombre_formateado = nombre.strip().replace(" ", "").lower()
#         regional_formateado = regional.strip().replace(" ", "").lower()
#         total_usuarios = Usuario.objects.count()
#         numero = total_usuarios + 1
#         password = f"{nombre_formateado}{regional_formateado}!{numero}"

#         try:
#             nuevo_usuario = Usuario(
#                 nombre_completo=nombre,
#                 correo=correo,
#                 regional=regional,
#                 password=password
#             )
#             nuevo_usuario.save()

#             # Enviar correo con credenciales
#             enviar_credenciales(destinatario=correo, nombre=nombre, correo=correo, password=password)

#             return f"Usuario registrado correctamente. Se enviaron las credenciales a: {correo}"

#         except NotUniqueError:
#             return "El correo ya está registrado", 400

#     return render_template('login.html', modo='registrar', regionales=regionales)


# # =============================================================
# # RUTA PARA INICIAR SESIÓN
# # =============================================================
# @app.route('/iniciarSesion', methods=['GET', 'POST'])
# def iniciarSesion():
#     """
#     Permite que el usuario inicie sesión con su correo y contraseña.
#     """
#     if request.method == 'POST':
#         correo = request.form['correo']
#         password = request.form['password']

#         try:
#             usuario = Usuario.objects.get(correo=correo)

#             if usuario.password == password:
#                 session['usuario_id'] = str(usuario.id)
#                 session['nombre'] = usuario.nombre_completo
#                 session['regional'] = usuario.regional

#                 return redirect(url_for('subir_guia'))  # Redirige al formulario de guías
#             else:
#                 return "Contraseña incorrecta", 401

#         except DoesNotExist:
#             return "Usuario no encontrado", 404

#     return render_template('login.html', modo='iniciar')

# @app.route('/cerrarSesion')
# def cerrarSesion():
#     """
#     Elimina los datos de sesión y redirige al login.
#     """
#     session.clear()
#     return redirect(url_for('iniciarSesion'))
