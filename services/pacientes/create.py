from flask import request, jsonify

def crear_paciente(mysql):  # Ahora mysql es pasado como parámetro
    try:
        # Obtener los datos del paciente desde el cuerpo de la solicitud
        data = request.get_json()
        nombre = data['nombre']
        apellidos = data['apellidos']
        fechaNacimiento = data['fechaNacimiento']
        direccion = data.get('direccion', None)
        telefono = data.get('telefono', None)

        # Crear una conexión con la base de datos
        cur = mysql.connection.cursor()
        
        # Verificar si ya existe un paciente con el mismo nombre y apellidos
        cur.execute("""
            SELECT idPaciente FROM paciente 
            WHERE nombre = %s AND apellidos = %s
        """, (nombre, apellidos))
        
        paciente_existente = cur.fetchone()
        
        if paciente_existente:
            cur.close()
            return jsonify({'error': 'Ya existe un paciente con ese nombre y apellidos'}), 400
        
        # Insertar los datos en la base de datos
        cur.execute("""
            INSERT INTO paciente (nombre, apellidos, fechaNacimiento, direccion, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, fechaNacimiento, direccion, telefono))

        # Confirmar los cambios en la base de datos
        mysql.connection.commit()
        cur.close()

        # Retornar una respuesta JSON
        return jsonify({'message': 'Paciente creado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400