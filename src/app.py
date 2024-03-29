"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from api.utils import APIException, generate_sitemap
from api.models import db
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_mail import Mail #IMPORTAR LA FUNCION Mail() de flask_mail

#from models import Person

ENV = os.getenv("FLASK_ENV")
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type = True)
db.init_app(app)

# Allow CORS requests to this API
CORS(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

mail_settings = {
    "MAIL_SERVER": 'sandbox.smtp.mailtrap.io',
    "MAIL_PORT":  2525,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.getenv('FLASK_MAIL_USERNAME'), #ACA COLOQUEN EL CORREO DE LA APP DEL ALUMN
    "MAIL_PASSWORD": os.getenv('FLASK_MAIL_PASSWORD'), #PASSWORD DEL CORREO DE LA APP DEL ALUMNO
    "MAIL_DEFAULT_SENDER": 'reservame@gmail.com'
}

app.config.update(mail_settings)
mail = Mail(app)
#agregan mail a la app y se va llamar en routes.py como current_app
app.mail= mail


# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

# def send_email(user):
#     token=user.get_token()
#     msg=Message("Password Reset Request", recipients=[user.email], sender="noreplay@codejana.com")
#     msg.body=f""" Para modificar tu contraseña, ingresa en el link que puedes ver abajo.
    
#     {url_for("reset_token" , token=token,_external=True)}
    
#     Si no has enviado una solicitud de restablecimiento de contraseña, por favor, ignora este mensaje.
    
#     ...
    
#     mail.send(msg)

# @app.route('/password', methods=[("GET","POST")])
# def reset_request():
#     form=ResetRequestForm()
#     if form.handleRecuperarPassword():
#         user=User.query.filter_by(email=form.email.data).first()
#             if user:
#             send_email(user)
#             flash("Le hemos enviado un correo para modificar su contraseña.","success")
#             return redirect(url_for("acceso"))
#     return render_template("password.html",title="Reset Request" , form=form, legend="Reset Request")

# @app.route('/password/<token>', methods=[("GET","POST")])
# def reset_token(token)
#     user=User.verify_token(token)
#     if user is None:
#         flash("Este enlace no es válido, o ha expirado. Por favor, inténtalo de nuevo" , "Warning")
#         return redirect(url_for("recuperar_password"))
    
#     form=ResetPasswordForm()
#     if form.handleRecuperarPassword():
#         hashed_password=bcrypt.generate_password_hash(form.password.data).decode("utf_8")
#         user.password=hashed_password
#         db.session.commit()
#         flash("Contraseña modificada con éxito. Ya puedes acceder de nuevo","success")
#         return redirect(url_for("acceso"))
#     return render_template("cambiar_password.html",title="cambiar_password",legend="cambiar_password",form=form)
              



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
