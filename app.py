from flask import Flask, abort, render_template, request, redirect, jsonify
from flask_login import LoginManager, login_required 
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from db import db 
from models import User # <--- Lo tuve que poner por separado ya que me daba un error constante

app = Flask(__name__)
# --------------------------------------------------------------
sentry_sdk.init(
    dsn="", integrations=[FlaskIntegration()]
)

file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)
# --------------------------------------------------------------
# Errores
@app.errorhandler(400)
def handle_400(e):
    app.logger.error(f"Error 400 detectado: {e.description}") # Para que quede en el registro 
    return render_template('400.html'), 400

@app.errorhandler(404)
def handle_404(e):
    app.logger.error(f"Error 404 - Ruta no encontrada: {request.path}")
    return render_template('404.html'), 404

@app.errorhandler(405)
def handle_405(e):
    app.logger.error(f"Error 405 - Método {request.method} no permitido en {request.path}")
    return render_template('405.html'), 405

@app.errorhandler(500)
def handle_500(e):
    app.logger.error(f"Error 500 Interno: {e}")
    return render_template('500.html'), 500

@app.errorhandler(HTTPException)
def handle_api_error(e):
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = 'application/json'
        return response
    return e

@app.route('/forzar-error')
def forzar_error():
    try:
        resultado = 1 / 0
    except Exception as e:
        app.logger.error(f"Error detectado: {e}")
        return "El error ha sido capturado y registrado en el log.", 500

# --------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos' # Nota para mi: Cambiar a esto si uso la laptop
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/juegos' # Cambiar a esto si uso la pc de escritorio
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hola123'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------------------------------------------------
# -Blueprint-
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from api.routes import api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

import controlador
# --------------------------------------------------------------
# Ruta para mostrar el formulario de agregar juego
@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

# Ruta para guardar juego
@app.route("/guardar_juego", methods=["POST"])
@login_required

def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

# Pantalla Principal que nos sirve para listar
@app.route("/")
@app.route("/juegos")
def juegos():
    juegos = controlador.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

# Ruta para eliminar juego
@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controlador.eliminar_juego(request.form["id"])
    return redirect("/juegos")

# Ruta para editar juego
@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    if id == 0:
        abort(400)
    juego = controlador.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

# Ruta para actualizar juego
@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

# --------------------------------------------------------------
# Iniciar la app
if __name__ == "__main__":
    app.run(port=8000, debug=True)