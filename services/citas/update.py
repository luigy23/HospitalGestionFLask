from flask import request, jsonify
from datetime import datetime, date

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

        # Validar el formato de la fecha y hora
        try:
            fecha_cita = datetime.strptime(fecha, '%Y-%m-%d').date()
            hora_cita = datetime.strptime(hora, '%H:%M').time()
        except ValueError:
            return jsonify({"message": "Formato inválido para fecha o hora"}), 400

        # Validar que la fecha no sea anterior a la fecha actual
        fecha_actual = date.today()
        if fecha_cita < fecha_actual:
            return jsonify({"error": "No se puede crear una cita con fecha pasada"}), 400

        # Crear una conexión con la base de datos
        cur = mysql.connection.cursor()

        # Verificar si ya existe una cita con el mismo doctor o paciente en ese horario
        # Excluyendo la cita actual que se está editando
        cur.execute("""
            SELECT idCita FROM cita 
            WHERE fecha = %s 
            AND hora = %s 
            AND (idDoctor = %s OR idPaciente = %s)
            AND idCita != %s
        """, (fecha_cita, hora_cita, doctor, paciente, idCita))
        
        cita_existente = cur.fetchone()
        
        if cita_existente:
            cur.close()
            return jsonify({'error': 'Ya existe una cita programada para ese doctor o paciente en ese horario'}), 400

        # Actualizar la cita en la base de datos
        cur.execute("""
            UPDATE cita
            SET fecha = %s, hora = %s, proposito = %s, estado = %s, idPaciente = %s, idDoctor = %s
            WHERE idCita = %s
        """, (fecha_cita, hora_cita, proposito, estado, paciente, doctor, idCita))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Cita actualizada con éxito"}), 200

    except Exception as e:
        return jsonify({"message": "Error al actualizar la cita", "error": str(e)}), 500



