from flask import request, jsonify
from datetime import datetime

def actualizar_cita(idCita, mysql):
    try:
        data = request.get_json()  # Obtener los datos del body de la solicitud
        fecha = data.get('fecha')
        hora = data.get('hora')
        proposito = data.get('proposito')
        estado = data.get('estado')
        paciente = data.get('paciente')
        doctor = data.get('doctor')

        # Verificar que todos los campos necesarios estén presentes
        if not all([fecha, hora, proposito, estado, paciente, doctor]):
            return jsonify({"message": "Faltan datos"}), 400

        # Actualizar la cita en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE cita
            SET fecha = %s, hora = %s, proposito = %s, estado = %s, idPaciente = %s, idDoctor = %s
            WHERE idCita = %s
        """, (fecha, hora, proposito, estado, paciente, doctor, idCita))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Cita actualizada con éxito"}), 200

    except Exception as e:
        return jsonify({"message": "Error al actualizar la cita", "error": str(e)}), 500



