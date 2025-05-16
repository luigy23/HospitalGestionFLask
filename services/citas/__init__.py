from flask import Blueprint
from .create import crear_cita
from .read import leer_citas, obtener_cita, enviar_paciente, enviar_doctor
from .update import actualizar_cita
from .delete import eliminar_cita

# Definir el Blueprint para el módulo 'citas'
citas_bp = Blueprint('citas', __name__)

# Registrar las rutas del Blueprint
def create_routes(mysql):
    # Definir las rutas y pasar mysql como argumento a las funciones
    citas_bp.add_url_rule('/crear', 'crear_cita', lambda: crear_cita(mysql), methods=['POST'])
    citas_bp.add_url_rule('/leer', 'leer_citas', lambda: leer_citas(mysql), methods=['GET'])
    citas_bp.add_url_rule('/leer/<int:idCita>', 'obtener_cita', lambda idCita: obtener_cita(idCita, mysql), methods=['GET'])
    citas_bp.add_url_rule('/enviar/pacientes', 'enviar_paciente', lambda: enviar_paciente(mysql), methods=['GET'])
    citas_bp.add_url_rule('/enviar/doctores', 'enviar_doctor', lambda: enviar_doctor(mysql), methods=['GET'])
    citas_bp.add_url_rule('/actualizar/<int:idCita>', 'actualizar_cita', lambda idCita: actualizar_cita(idCita, mysql), methods=['PUT'])
    citas_bp.add_url_rule('/eliminar/<int:idCita>', 'eliminar_cita', lambda idCita: eliminar_cita(idCita, mysql), methods=['DELETE'])


