from flask import jsonify
from mysql.connector.errors import Error

def leer_pacientes(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM paciente")
        pacientes = cur.fetchall()
        cur.close()

        if not pacientes:
            return jsonify({"message": "No se encontraron pacientes"}), 404

        # Convertir los resultados a un formato que pueda ser utilizado en el frontend
        pacientes_list = [
            {
                'idPaciente': paciente[0],
                'nombre': paciente[1],
                'apellidos': paciente[2],
                'fechaNacimiento': paciente[3].strftime('%Y-%m-%d') if paciente[3] else None,
                'direccion': paciente[4],
                'telefono': paciente[5],
            }
            for paciente in pacientes
        ]

        return jsonify({'pacientes': pacientes_list}), 200

    except Error as e:
        print(f"Error al leer pacientes: {e}")
        return jsonify({"message": "Hubo un problema al leer los pacientes"}), 500


def obtener_paciente(idPaciente, mysql):
    try:
        if not isinstance(idPaciente, int) or idPaciente <= 0:
            return jsonify({"message": "ID de paciente inválido"}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM paciente WHERE idPaciente = %s", (idPaciente,))
        paciente = cur.fetchone()
        cur.close()

        if paciente:
            return jsonify({
                'idPaciente': paciente[0],
                'nombre': paciente[1],
                'apellidos': paciente[2],
                'fechaNacimiento': paciente[3].strftime('%Y-%m-%d') if paciente[3] else None,
                'direccion': paciente[4],
                'telefono': paciente[5],
            }), 200
        else:
            return jsonify({"message": "Paciente no encontrado"}), 404

    except Error as e:
        print(f"Error al obtener paciente: {e}")
        return jsonify({"message": "Hubo un problema al obtener el paciente"}), 500
