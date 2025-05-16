from flask import jsonify
from mysql.connector.errors import Error
from datetime import datetime

def leer_tratamientos(mysql):
    try:
        query = """
                SELECT 
                    t.codigoTratamiento, t.nombre, t.descripcion, t.duracion,
                    p.nombre AS nombre_paciente, p.apellidos AS apellidos_paciente
                FROM tratamiento t
                JOIN paciente p ON t.idPaciente = p.idPaciente
            """
        
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        tratamientos = cursor.fetchall()
        tratamientos_list = []

        for tratamiento in tratamientos:
            tratamientos_list.append({
                'codigoTratamiento' : tratamiento[0],
                'nombre': tratamiento[1],
                'descripcion': tratamiento[2],
                'duracion': tratamiento[3],
                'paciente': f"{tratamiento[4]} {tratamiento[5]}" if tratamiento[4] and tratamiento[5] else 'Paciente no asignado',
            })
        cursor.close()
        
        return jsonify({'tratamientos': tratamientos_list}), 200
    except Error as e:
        print(f"Error al leer tratamientos: {e}")
        return jsonify({"message": "Hubo un problema al leer los tratamientos"}), 500

def obtener_tratamiento(idTratamiento, mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT codigoTratamiento, nombre, duracion, descripcion FROM tratamiento WHERE codigoTratamiento = %s", (idTratamiento,))
        tratamiento = cur.fetchone()
        cur.close()
        if tratamiento:
            return jsonify({'codigoTratamiento': tratamiento[0], 
                            'nombre': tratamiento[1], 
                            'duracion': tratamiento[2],
                            'descripcion': tratamiento[3]}), 200
        else:
            return jsonify({"message": "Tratamiento no encontrado"}), 404
    except Exception as e:
        return jsonify({'message': f'Error al obtener tratamientos: {e}'}), 500

def enviar_paciente(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT idPaciente, nombre, apellidos FROM paciente")
        pacientes = cur.fetchall()
        cur.close()

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