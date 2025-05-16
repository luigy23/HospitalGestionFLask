from flask import jsonify

def eliminar_cita(idCita, mysql):
    try:
        cursor = mysql.connection.cursor()
        query = "DELETE FROM cita WHERE idCita = %s"
        cursor.execute(query, (idCita,))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Cita no encontrada'}), 404

        return jsonify({'message': f'Cita con ID {id} eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
