from flask import jsonify
from mysql.connector import Error

def leer_doctores(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM doctor")
        doctores = cur.fetchall()
        cur.close()

        if not doctores:
            return jsonify({"message": "No se encontraron doctores"}), 404

        # Convertir los resultados a un formato que pueda ser utilizado en el frontend
        doctores_list = [
            {
                'idDoctor': doctor[0],
                'nombre': doctor[1],
                'apellidos': doctor[2],
                'licencia': doctor[3],
                'especialidad': doctor[4] if doctor[4] else None,
                'telefono': doctor[5] if doctor[5] else None,
            }
            for doctor in doctores
        ]

        return jsonify({'doctores': doctores_list}), 200

    except Error as e:
        print(f"Error al leer doctores: {e}")
        return jsonify({"message": "Hubo un problema al leer los doctores"}), 500


def obtener_doctor(idDoctor, mysql):
    try:
        if not isinstance(idDoctor, int) or idDoctor <= 0:
            return jsonify({"message": "ID de doctor inválido"}), 400

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM doctor WHERE idDoctor = %s", (idDoctor,))
        doctor = cur.fetchone()
        cur.close()

        if doctor:
            return jsonify({
                'idDoctor': doctor[0],
                'nombre': doctor[1],
                'apellidos': doctor[2],
                'licencia': doctor[3],
                'especialidad': doctor[4] if doctor[4] else None,
                'telefono': doctor[5] if doctor[5] else None,
            }), 200
        else:
            return jsonify({"message": "Doctor no encontrado"}), 404

    except Error as e:
        print(f"Error al obtener doctor: {e}")
        return jsonify({"message": "Hubo un problema al obtener el doctor"}), 500

