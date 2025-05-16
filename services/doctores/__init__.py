from flask import Blueprint
from .create import crear_doctor
from .read import leer_doctores, obtener_doctor
from .update import actualizar_doctor
from .delete import eliminar_doctor

# Definir el Blueprint para el módulo 'doctores'
doctores_bp = Blueprint('doctores', __name__)

# Registrar las rutas del Blueprint
def create_routes(mysql):
    # Definir las rutas y pasar mysql como argumento a las funciones
    doctores_bp.add_url_rule('/crear', 'crear_doctor', lambda: crear_doctor(mysql), methods=['POST'])
    doctores_bp.add_url_rule('/leer', 'leer_doctores', lambda: leer_doctores(mysql), methods=['GET'])
    doctores_bp.add_url_rule('/leer/<int:idDoctor>', 'obtener_doctor', lambda idDoctor: obtener_doctor(idDoctor, mysql), methods=['GET'])
    doctores_bp.add_url_rule('/actualizar/<int:idDoctor>', 'actualizar_doctor', lambda idDoctor: actualizar_doctor(idDoctor,mysql), methods=['PUT'])
    doctores_bp.add_url_rule('/eliminar/<int:idDoctor>', 'eliminar_doctor', lambda idDoctor: eliminar_doctor(idDoctor, mysql), methods=['DELETE'])



