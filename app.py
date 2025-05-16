from flask import Flask, render_template
from flask_mysqldb import MySQL
from services.pacientes import pacientes_bp, create_routes as pacientes_create_routes
from services.doctores import doctores_bp, create_routes as doctores_create_routes
from services.citas import citas_bp, create_routes as citas_create_routes
from services.tratamientos import tratamientos_bp, create_routes as tratamientos_create_routes
from config import Config

mysql = MySQL()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)  # Cargar configuración desde el archivo Config
    mysql.init_app(app)  # Inicializar la conexión MySQL con la app

    # Registrar los blueprints y pasar la conexión mysql a las rutas
    pacientes_create_routes(mysql)
    doctores_create_routes(mysql)
    citas_create_routes(mysql)
    tratamientos_create_routes(mysql)

    # Registrar los blueprints en la aplicación Flask
    app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
    app.register_blueprint(doctores_bp, url_prefix='/doctores')
    app.register_blueprint(citas_bp, url_prefix='/citas')
    app.register_blueprint(tratamientos_bp, url_prefix='/tratamientos')

    # Rutas principales de la aplicación
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/pacientes')
    def pacientes():
        return render_template('pacientes.html')

    @app.route('/doctores')
    def doctores():
        return render_template('doctores.html')

    @app.route('/citas')
    def citas():
        return render_template('citas.html')

    @app.route('/tratamientos')
    def tratamientos():
        return render_template('tratamientos.html')

    @app.route('/habitaciones')
    def habitaciones():
        return render_template('habitaciones.html')

    @app.route('/internamientos')
    def internamientos():
        return render_template('internamientos.html')

    return app, mysql

# Ejecutar la aplicación
if __name__ == '__main__':
    app, mysql = create_app()  # Crear la app y obtener la conexión mysql
    app.run(debug=True)



