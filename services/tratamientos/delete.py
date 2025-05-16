from flask import jsonify

def eliminar_tratamiento(codigoTratamiento, mysql):
    try:
        # Eliminar el tratamiento de la base de datos
        query = "DELETE FROM tratamiento WHERE codigoTratamiento = %s"
        
        cursor = mysql.connection.cursor()
        cursor.execute(query, (codigoTratamiento,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'message': 'Tratamiento eliminado exitosamente', 'status': 200}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'status': 400}), 400

