from flask import jsonify, request

def actualizar_paciente(idPaciente, mysql):
    # Obtener los nuevos datos del paciente
    nombre = request.json.get('nombre')
    apellidos = request.json.get('apellidos')
    fechaNacimiento = request.json.get('fechaNacimiento')
    direccion = request.json.get('direccion', None)  # Puede ser None
    telefono = request.json.get('telefono', None)    # Puede ser None

    # Actualizar el paciente en la base de datos
    cur = mysql.connection.cursor()
    print("antes")
    cur.execute("""
        UPDATE paciente
        SET nombre = %s, apellidos = %s, fechaNacimiento = %s, direccion = %s, telefono = %s
        WHERE idPaciente = %s
    """, (nombre, apellidos, fechaNacimiento, direccion, telefono, idPaciente))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Paciente actualizado exitosamente"}), 200
