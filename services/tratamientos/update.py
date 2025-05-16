from flask import request, jsonify
from werkzeug.exceptions import BadRequest

def actualizar_tratamiento(codigoTratamiento, mysql):
    try:
        # Obtener los datos del tratamiento a actualizar
        data = request.get_json()
        
        # Validar que los datos existan
        if 'nombre' not in data or 'descripcion' not in data or 'duracion' not in data:
            raise BadRequest("Faltan datos obligatorios (nombre, descripcion, duracion)")
        
        # Actualizar el tratamiento en la base de datos
        query = """
        UPDATE tratamiento
        SET nombre = %s, descripcion = %s, duracion = %s
        WHERE codigoTratamiento = %s
        """
        values = (data['nombre'], data['descripcion'], data['duracion'], codigoTratamiento)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Tratamiento actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400




