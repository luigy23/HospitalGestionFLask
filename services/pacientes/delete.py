from flask import jsonify

def eliminar_paciente(idPaciente, mysql):
    cur = mysql.connection.cursor()

    # Verificar si el paciente existe
    cur.execute("SELECT idPaciente FROM paciente WHERE idPaciente = %s", (idPaciente,))
    paciente = cur.fetchone()

    if not paciente:
        cur.close()
        return jsonify({"message": "Paciente no encontrado"}), 404

    # Eliminar el paciente
    cur.execute("DELETE FROM paciente WHERE idPaciente = %s", (idPaciente,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Paciente eliminado exitosamente"}), 200

