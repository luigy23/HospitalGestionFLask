from flask import Blueprint
from .create import crear_paciente
from .read import leer_pacientes, obtener_paciente
from .update import actualizar_paciente
from .delete import eliminar_paciente

# Crear el Blueprint para el módulo de pacientes
pacientes_bp = Blueprint('pacientes', __name__)

# Registrar las rutas del Blueprint
def create_routes(mysql):
    # Definir las rutas y pasar mysql como argumento a las funciones
    pacientes_bp.add_url_rule('/crear', 'crear_paciente', lambda: crear_paciente(mysql), methods=['POST'])
    pacientes_bp.add_url_rule('/leer', 'leer_pacientes', lambda: leer_pacientes(mysql), methods=['GET'])
    pacientes_bp.add_url_rule('/leer/<int:idPaciente>', 'obtener_paciente', lambda idPaciente: obtener_paciente(idPaciente, mysql), methods=['GET'])
    pacientes_bp.add_url_rule('/actualizar/<int:idPaciente>', 'actualizar_paciente', lambda idPaciente: actualizar_paciente(idPaciente, mysql), methods=['PUT'])
    pacientes_bp.add_url_rule('/eliminar/<int:idPaciente>', 'eliminar_paciente', lambda idPaciente: eliminar_paciente(idPaciente, mysql), methods=['DELETE'])


