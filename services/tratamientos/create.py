from flask import request, jsonify

def crear_tratamiento(mysql):
    try:
        # Obtener los datos del tratamiento desde el cuerpo de la solicitud
        data = request.get_json()
        
        # Validar los datos recibidos
        if not all(key in data for key in ['nombre', 'descripcion', 'duracion', 'idPaciente']):
            return jsonify({"message": "Todos los campos son requeridos: nombre, descripcion, duracion, idPaciente"}), 400
        
        # Insertar el tratamiento en la base de datos
        query = "INSERT INTO tratamiento (nombre, descripcion, duracion,idPaciente) VALUES (%s, %s, %s, %s)"
        values = (data['nombre'], data['descripcion'], data['duracion'], data['idPaciente'])
        
        # Insertar los datos en la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Tratamiento registrado exitosamente', 'status': 201}), 201
    except Exception as e:
        return jsonify({'error': str(e), 'status': 400}), 400


