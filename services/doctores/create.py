from flask import request, jsonify

def crear_doctor(mysql):  # Ahora mysql es pasado como parámetro
    try:
        # Obtener los datos del doctor desde el cuerpo de la solicitud
        data = request.get_json()
        nombre = data['nombre']
        apellidos = data['apellidos']
        licencia = data['licencia']
        especialidad = data.get('especialidad')
        telefono = data.get('telefono', None)

        # Crear una conexión con la base de datos
        cur = mysql.connection.cursor()
        
        # Insertar los datos en la base de datos
        cur.execute("""
            INSERT INTO doctor (nombre, apellidos, licencia, especialidad, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, licencia, especialidad, telefono))

        # Confirmar los cambios en la base de datos
        mysql.connection.commit()
        cur.close()

        # Retornar una respuesta JSON
        return jsonify({'message': 'Doctor creado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
