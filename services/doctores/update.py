from flask import request, jsonify

def actualizar_doctor(idDoctor, mysql):
    # Obtener los nuevos datos del doctor
    nombre = request.json.get('nombre')
    apellidos = request.json.get('apellidos')
    licencia = request.json.get('licencia')
    especialidad = request.json.get('especialidad')
    telefono = request.json.get('telefono', None)    # Puede ser None

    # Actualizar el doctor en la base de datos
    cur = mysql.connection.cursor()
    print("antes")
    cur.execute("""
        UPDATE doctor
        SET nombre = %s, apellidos = %s, licencia = %s, especialidad = %s, telefono = %s
        WHERE idDoctor = %s
    """, (nombre, apellidos, licencia, especialidad, telefono, idDoctor))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Doctor actualizado exitosamente"}), 200