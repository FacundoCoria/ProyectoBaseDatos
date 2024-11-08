from flask import Flask, request, jsonify
from login import connect_to_database
from mysql.connector import Error

app = Flask(__name__)

def validar_fecha(fecha):
    partes = fecha.split('-')
    if len(partes) == 3:
        año, mes, día = partes
        if len(año) == 4 and año.isdigit() and len(mes) == 2 and mes.isdigit() and len(día) == 2 and día.isdigit():
            return True
    return False

@app.route('/registrar_alumno', methods=['POST'])
def registrar_alumno():
    data = request.json
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fecha = data.get('fecha')

    if not validar_fecha(fecha):
        return jsonify({"error": "Fecha no válida. Debe estar en formato YYYY-MM-DD"}), 400

    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO alumnos (ci, nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (ci, nombre, apellido, fecha))
        connection.commit()
        return jsonify({"message": "Alumno registrado exitosamente."}), 201
    except Error as e:
        return jsonify({"error": f"Error al registrar el alumno: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/eliminar_alumno', methods=['DELETE'])
def eliminar_alumno():
    data = request.json
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fecha = data.get('fecha')

    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM alumnos WHERE ci = %s AND nombre = %s AND apellido = %s AND fecha_nacimiento = %s"
        cursor.execute(query, (ci, nombre, apellido, fecha))
        connection.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": "Alumno eliminado exitosamente."}), 200
        else:
            return jsonify({"error": "No se encontró el alumno."}), 404
    except Error as e:
        return jsonify({"error": f"Error al eliminar el alumno: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/clases_disponibles', methods=['GET'])
def mostrar_clases_disponibles():
    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        cursor = connection.cursor()
        query = """
        SELECT clase.id, actividades.descripcion, turnos.hora_inicio, turnos.hora_fin, clase.tipo_clase
        FROM clase
        JOIN actividades ON clase.id_actividad = actividades.id
        JOIN turnos ON clase.id_turno = turnos.id
        WHERE clase.dictada = FALSE
        """
        cursor.execute(query)
        clases = cursor.fetchall()

        if clases:
            clases_disponibles = [
                {"id": clase[0], "descripcion": clase[1], "hora_inicio": clase[2], "hora_fin": clase[3], "tipo": clase[4]}
                for clase in clases
            ]
            return jsonify(clases_disponibles), 200
        else:
            return jsonify({"message": "No hay clases disponibles."}), 404
    except Error as e:
        return jsonify({"error": f"Error al mostrar las clases: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/unirse_clase', methods=['POST'])
def unirse_clase():
    data = request.json
    ci = data.get('ci')
    id_clase = data.get('id_clase')

    connection = connect_to_database()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        cursor = connection.cursor()
        query_verificar = "SELECT * FROM alumno_clase WHERE id_clase = %s AND ci_alumno = %s"
        cursor.execute(query_verificar, (id_clase, ci))
        resultado = cursor.fetchone()

        if resultado:
            return jsonify({"message": "El alumno ya está registrado en esta clase."}), 400
        else:
            query_insertar = "INSERT INTO alumno_clase (id_clase, ci_alumno) VALUES (%s, %s)"
            cursor.execute(query_insertar, (id_clase, ci))
            connection.commit()
            return jsonify({"message": "Alumno agregado a la clase exitosamente."}), 201
    except Error as e:
        return jsonify({"error": f"Error al agregar el alumno a la clase: {e}"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
