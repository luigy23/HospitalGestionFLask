from flask import request, jsonify
from datetime import datetime, date

def crear_cita(mysql):
    try:
        # Obtener los datos del request
        data = request.get_json()

        # Validar que todos los campos necesarios estén presentes
        if not all(key in data for key in ['fecha', 'hora', 'proposito', 'idPaciente', 'idDoctor']):
            return jsonify({"message": "Todos los campos son requeridos: fecha, hora, propósito, idPaciente, idDoctor"}), 400

        # Validar el formato de la fecha y hora
        try:
            fecha_cita = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
            hora_cita = datetime.strptime(data['hora'], '%H:%M').time()
        except ValueError:
            return jsonify({"message": "Formato inválido para fecha o hora"}), 400

        # Validar que la fecha no sea anterior a la fecha actual
        fecha_actual = date.today()
        if fecha_cita < fecha_actual:
            return jsonify({"error": "No se puede crear una cita con fecha pasada"}), 400

        # Crear una conexión con la base de datos
        cur = mysql.connection.cursor()

        # Verificar si ya existe una cita con el mismo doctor, paciente y hora
        cur.execute("""
            SELECT idCita FROM cita 
            WHERE fecha = %s 
            AND hora = %s 
            AND (idDoctor = %s OR idPaciente = %s)
        """, (fecha_cita, hora_cita, data['idDoctor'], data['idPaciente']))
        
        cita_existente = cur.fetchone()
        
        if cita_existente:
            cur.close()
            return jsonify({'error': 'Ya existe una cita programada para ese doctor o paciente en ese horario'}), 400

        # Insertar los datos en la base de datos
        cur.execute("""
            INSERT INTO cita (fecha, hora, proposito, estado, idPaciente, idDoctor) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fecha_cita, hora_cita, data['proposito'], 'Pendiente', data['idPaciente'], data['idDoctor']))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Cita creada con éxito"}), 201

    except Exception as e:
        print(f"Error al crear la cita: {e}")
        return jsonify({"message": f"Error al crear la cita: {str(e)}"}), 500

