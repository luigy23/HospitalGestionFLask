from flask import jsonify
from mysql.connector.errors import Error
from datetime import datetime

def leer_citas(mysql):
    try:
        cursor = mysql.connection.cursor()
        query = """
            SELECT 
                c.idCita, c.fecha, c.hora, c.proposito, c.estado,
                p.nombre AS nombre_paciente, p.apellidos AS apellidos_paciente,
                d.nombre AS nombre_doctor, d.apellidos AS apellidos_doctor
            FROM cita c
            JOIN paciente p ON c.idPaciente = p.idPaciente
            JOIN doctor d ON c.idDoctor = d.idDoctor
        """
        cursor.execute(query)
        citas = cursor.fetchall()
        cursor.close()

        # Convertir las citas en un formato adecuado para el frontend
        citas_list = []
        for cita in citas:
            # Convertir `hora` de timedelta a formato 12 horas con A.M. / P.M.
            if cita[2]:  # Si hay un valor para `hora`
                total_seconds = cita[2].seconds
                hours = total_seconds // 3600
                minutes = (total_seconds // 60) % 60
                period = "A.M." if hours < 12 else "P.M."
                formatted_hours = hours % 12 if hours % 12 != 0 else 12  # Convertir a formato 12 horas
                hora_str = f"{formatted_hours:02}:{minutes:02} {period}"
            else:
                hora_str = 'Hora no disponible'

            citas_list.append({
                'idCita': cita[0],
                'fecha': cita[1].strftime('%Y-%m-%d') if cita[1] else 'Fecha no disponible',
                'hora': hora_str,
                'proposito': cita[3] if cita[3] else 'Propósito no definido',
                'estado': cita[4] if cita[4] else 'Estado no definido',
                'paciente': f"{cita[5]} {cita[6]}" if cita[5] and cita[6] else 'Paciente no asignado',
                'doctor': f"{cita[7]} {cita[8]}" if cita[7] and cita[8] else 'Doctor no asignado'
            })

        return jsonify({'citas': citas_list}), 200
    except Error as e:
        print(f"Error al leer citas: {e}")
        return jsonify({"message": "Hubo un problema al leer las citas"}), 500

def enviar_paciente(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT idPaciente, nombre, apellidos FROM paciente")
        pacientes = cur.fetchall()
        cur.close()

        # Convertir los resultados a un formato adecuado para el frontend
        pacientes_list = [
            {
                'idPaciente': paciente[0],
                'nombre': paciente[1] + ' ' + paciente[2]  # Concatenar nombre y apellidos
            }
            for paciente in pacientes
        ]

        return jsonify({'pacientes': pacientes_list}), 200
    except Error as e:
        print(f"Error al obtener pacientes: {e}")
        return jsonify({"message": "Hubo un problema al obtener los pacientes"}), 500
    
def obtener_cita(idCita, mysql):
    try:
        # Verificar que el ID de la cita sea válido
        if not isinstance(idCita, int) or idCita <= 0:
            return jsonify({"message": "ID de cita inválido"}), 400

        # Conectar a la base de datos
        cur = mysql.connection.cursor()
        
        # Ejecutar la consulta para obtener la cita por ID
        cur.execute("""
            SELECT c.idCita, c.fecha, c.hora, c.proposito, c.estado, c.idPaciente, c.idDoctor,
                   p.nombre AS paciente_nombre, p.apellidos AS paciente_apellidos,
                   d.nombre AS doctor_nombre, d.apellidos AS doctor_apellidos
            FROM cita c
            LEFT JOIN paciente p ON c.idPaciente = p.idPaciente
            LEFT JOIN doctor d ON c.idDoctor = d.idDoctor
            WHERE c.idCita = %s
        """, (idCita,))
        cita = cur.fetchone()
        
        # Cerrar la conexión con la base de datos
        cur.close()

        # Si la cita existe, devolver los datos formateados
        if cita:
            # Convertir los valores de fecha y hora a strings si son tipos de datos datetime o timedelta
            fecha = cita[1].strftime('%Y-%m-%d') if isinstance(cita[1], datetime) else str(cita[1])
            hora = cita[2].strftime('%H:%M:%S') if isinstance(cita[2], datetime) else str(cita[2])

            return jsonify({
                'idCita': cita[0],
                'fecha': fecha,
                'hora': hora,  # Asegurarse de que la hora esté formateada correctamente
                'proposito': cita[3],
                'estado': cita[4],
                'idPaciente': cita[5],
                'idDoctor': cita[6],
                'paciente': f"{cita[7]} {cita[8]}",  # Nombre completo del paciente
                'doctor': f"{cita[9]} {cita[10]}"   # Nombre completo del doctor
            }), 200
        else:
            # Si no se encuentra la cita
            return jsonify({"message": "Cita no encontrada"}), 404

    except Error as e:
        # Manejo de errores de base de datos
        print(f"Error al obtener cita: {e}")
        return jsonify({"message": "Hubo un problema al obtener la cita"}), 500
def enviar_doctor(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT idDoctor, nombre, apellidos FROM doctor")
        doctores = cur.fetchall()
        cur.close()

        # Convertir los resultados a un formato adecuado para el frontend
        doctores_list = [
            {
                'idDoctor': doctor[0],
                'nombre': doctor[1] + ' ' + doctor[2]  # Concatenar nombre y apellidos
            }
            for doctor in doctores
        ]

        return jsonify({'doctores': doctores_list}), 200
    except Error as e:
        print(f"Error al obtener doctores: {e}")
        return jsonify({"message": "Hubo un problema al obtener los doctores"}), 500