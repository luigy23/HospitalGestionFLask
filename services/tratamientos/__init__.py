from flask import Blueprint
from .create import crear_tratamiento
from .read import leer_tratamientos, enviar_paciente, obtener_tratamiento
from .update import actualizar_tratamiento
from .delete import eliminar_tratamiento

# Crear el Blueprint para el módulo de tratamientos
tratamientos_bp = Blueprint('tratamientos', __name__)

# Registrar las rutas del Blueprint
def create_routes(mysql):
    # Definir las rutas y pasar mysql como argumento a las funciones
    tratamientos_bp.add_url_rule('/crear', 'crear_tratamiento', lambda: crear_tratamiento(mysql), methods=['POST'])
    tratamientos_bp.add_url_rule('/leer', 'leer_tratamientos', lambda: leer_tratamientos(mysql), methods=['GET'])
    tratamientos_bp.add_url_rule('/enviar/pacientes', 'enviar_paciente', lambda: enviar_paciente(mysql), methods=['GET'])
    tratamientos_bp.add_url_rule('/leer/<int:codigoTratamiento>', 'obtener_tratamiento', lambda codigoTratamiento: obtener_tratamiento(codigoTratamiento, mysql), methods=['GET'])
    tratamientos_bp.add_url_rule('/actualizar/<int:codigoTratamiento>', 'actualizar_tratamiento', lambda codigoTratamiento: actualizar_tratamiento(codigoTratamiento, mysql), methods=['PUT'])
    tratamientos_bp.add_url_rule('/eliminar/<int:codigoTratamiento>', 'eliminar_tratamiento', lambda codigoTratamiento: eliminar_tratamiento(codigoTratamiento, mysql), methods=['DELETE'])



