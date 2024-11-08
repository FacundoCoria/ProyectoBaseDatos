from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from basedatos import connect_to_database
from mysql.connector import Error

# Crear el blueprint para el estudiante
estudiante_blueprint = Blueprint('estudiante', __name__)

def validar_fecha(fecha):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    partes = fecha.split('-')
    if len(partes) == 3:
        año, mes, día = partes
        if len(año) == 4 and año.isdigit() and len(mes) == 2 and mes.isdigit() and len(día) == 2 and día.isdigit():
            return True
    return False

def registrar_alumno(ci, nombre, apellido, fecha):
    """Registra un alumno en la base de datos."""
    if not validar_fecha(fecha):
        return {"error": "Fecha no válida. Debe estar en formato YYYY-MM-DD"}, 400
    
    connection = connect_to_database()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos."}, 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO alumnos (ci, nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (ci, nombre, apellido, fecha))
        connection.commit()
        return {"message": "Alumno registrado exitosamente."}, 201
    except Error as e:
        return {"error": f"Error al registrar el alumno: {e}"}, 500
    finally:
        cursor.close()
        connection.close()

def eliminar_alumno(ci, nombre, apellido, fecha):
    """Elimina un alumno de la base de datos."""
    connection = connect_to_database()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos."}, 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM alumnos WHERE ci = %s AND nombre = %s AND apellido = %s AND fecha_nacimiento = %s"
        cursor.execute(query, (ci, nombre, apellido, fecha))
        connection.commit()
        
        if cursor.rowcount > 0:
            return {"message": "Alumno eliminado exitosamente."}, 200
        else:
            return {"error": "No se encontró el alumno."}, 404
    except Error as e:
        return {"error": f"Error al eliminar el alumno: {e}"}, 500
    finally:
        cursor.close()
        connection.close()

def obtener_clases_disponibles():
    """Obtiene las clases disponibles de la base de datos."""
    connection = connect_to_database()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos."}, 500

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
            return clases_disponibles, 200
        else:
            return {"message": "No hay clases disponibles."}, 404
    except Error as e:
        return {"error": f"Error al mostrar las clases: {e}"}, 500
    finally:
        cursor.close()
        connection.close()

def unirse_a_clase(ci, id_clase):
    """Permite que un alumno se una a una clase."""
    connection = connect_to_database()
    if connection is None:
        return {"error": "No se pudo conectar a la base de datos."}, 500

    try:
        cursor = connection.cursor()
        query_verificar = "SELECT * FROM alumno_clase WHERE id_clase = %s AND ci_alumno = %s"
        cursor.execute(query_verificar, (id_clase, ci))
        resultado = cursor.fetchone()

        if resultado:
            return {"message": "El alumno ya está registrado en esta clase."}, 400
        else:
            query_insertar = "INSERT INTO alumno_clase (id_clase, ci_alumno) VALUES (%s, %s)"
            cursor.execute(query_insertar, (id_clase, ci))
            connection.commit()
            return {"message": "Alumno agregado a la clase exitosamente."}, 201
    except Error as e:
        return {"error": f"Error al agregar el alumno a la clase: {e}"}, 500
    finally:
        cursor.close()
        connection.close()

# Rutas de estudiante

@estudiante_blueprint.route('/estudiante/menu', methods=['GET'])
def estudiante_menu():
    return render_template('estudiante_menu.html')

@estudiante_blueprint.route('/estudiante/registrar', methods=['POST'])
def registrar_alumno_route():
    data = request.json
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fecha = data.get('fecha')

    response, status = registrar_alumno(ci, nombre, apellido, fecha)
    return jsonify(response), status

@estudiante_blueprint.route('/estudiante/eliminar', methods=['POST'])
def eliminar_alumno_route():
    data = request.json
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    fecha = data.get('fecha')

    response, status = eliminar_alumno(ci, nombre, apellido, fecha)
    return jsonify(response), status

@estudiante_blueprint.route('/estudiante/clases_disponibles', methods=['GET'])
def clases_disponibles_route():
    response, status = obtener_clases_disponibles()
    return jsonify(response), status

@estudiante_blueprint.route('/estudiante/unirse', methods=['POST'])
def unirse_a_clase_route():
    data = request.json
    ci = data.get('ci')
    id_clase = data.get('id_clase')

    response, status = unirse_a_clase(ci, id_clase)
    return jsonify(response), status
