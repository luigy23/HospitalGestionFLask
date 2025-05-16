from flask import jsonify

def eliminar_doctor(idDoctor, mysql):
    cur = mysql.connection.cursor()

    cur.execute("SELECT idDoctor FROM doctor WHERE idDoctor = %s", (idDoctor,))
    doctor = cur.fetchone()

    if not doctor:
        cur.close()
        return jsonify({"message": "Doctor no encontrado"}), 404

    # Eliminar el doctor
    cur.execute("DELETE FROM doctor WHERE idDoctor = %s", (idDoctor,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Doctor eliminado exitosamente"}), 200
