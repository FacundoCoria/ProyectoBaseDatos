from flask import Blueprint, request, render_template, redirect, url_for, flash
from basedatos import connect_to_database
from mysql.connector import Error

# Crear el blueprint para equipamiento
equipamiento_blueprint = Blueprint('equipamiento', __name__)

@equipamiento_blueprint.route('/equipamiento/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno_clase_route():
    connection = connect_to_database()
    if connection is None:
        flash("No se pudo conectar a la base de datos.", "error")
        return redirect(url_for('equipamiento.registrar_alumno_clase_route'))

    if request.method == 'POST':
        data = request.form
        id_clase = data.get('id_clase')
        ci_alumno = data.get('ci_alumno')
        id_turno = data.get('id_turno')  # Obtener el valor de id_turno
        id_equipamiento = data.get('id_equipamiento', None)
        es_alquilado = 'es_alquilado' in data

        if not id_clase or not ci_alumno or not id_turno:  # Validar que el id_turno también esté presente
            flash("Debe proporcionar id_clase, ci_alumno y id_turno.", "error")
            return redirect(url_for('equipamiento.registrar_alumno_clase_route'))

        try:
            cursor = connection.cursor()

            # Verificar si el equipamiento es alquilado y obtener el costo del alquiler
            costo_alquiler = 0.0
            if es_alquilado and id_equipamiento:
                query = "SELECT costo FROM equipamiento WHERE id = %s"
                cursor.execute(query, (id_equipamiento,))
                resultado = cursor.fetchone()
                if resultado:
                    costo_alquiler = resultado[0]

            # Insertar el registro en la tabla alumno_clase, incluyendo id_turno
            query = """
                INSERT INTO alumno_clase (id_clase, ci_alumno, id_turno, id_equipamiento, costo_adicional)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_alumno, id_turno, id_equipamiento, costo_alquiler if es_alquilado else 0.0))
            connection.commit()
            flash("Alumno registrado exitosamente en la clase.", "success")
        except Error as e:
            flash(f"Error al registrar al alumno en la clase: {e}", "error")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('equipamiento.registrar_alumno_clase_route'))

    # Obtener el listado de clases, alumnos y equipamientos para mostrar en el formulario
    try:
        cursor = connection.cursor()

        # Obtener los alumnos disponibles
        cursor.execute("SELECT ci, nombre FROM alumnos")
        alumnos = cursor.fetchall()

        # Obtener las clases disponibles
        cursor.execute("SELECT id, nombre FROM clase")
        clases = cursor.fetchall()

        # Obtener los equipamientos disponibles
        cursor.execute("SELECT id, descripcion FROM equipamiento")
        equipamientos = cursor.fetchall()

        # Obtener los turnos disponibles
        cursor.execute("SELECT id, descripcion FROM turno")
        turnos = cursor.fetchall()  # Asumiendo que hay una tabla 'turno'
    except Error as e:
        flash(f"Error al obtener datos de la base de datos: {e}", "error")
        alumnos, clases, equipamientos, turnos = [], [], [], []
    finally:
        cursor.close()
        connection.close()

    return render_template('registrar_alumno_clase.html', alumnos=alumnos, clases=clases, equipamientos=equipamientos, turnos=turnos)


@equipamiento_blueprint.route('/equipamiento/adquirir', methods=['POST'])
def adquirir_equipamiento():
    connection = connect_to_database()
    if connection is None:
        flash("Error al conectar a la base de datos.", "error")
        return redirect(url_for('equipamiento.registrar_alumno_clase_route'))  # Redirigir al formulario de registro si no se conecta

    try:
        data = request.form
        ci_alumno = data['ci_alumno']
        id_clase = data['id_clase']
        id_equipamiento = data.get('id_equipamiento')
        es_alquilado = 'es_alquilado' in data

        cursor = connection.cursor()

        # Verificar si el equipo es alquilado y obtener el costo de alquiler
        costo_alquiler = 0.0
        if es_alquilado:
            query = "SELECT costo FROM equipamiento WHERE id = %s"
            cursor.execute(query, (id_equipamiento,))
            result = cursor.fetchone()
            if result:
                costo_alquiler = result[0]

        # Registrar el equipo en la tabla `alumno_clase`
        query = """
            INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento, costo_adicional)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_clase, ci_alumno, id_equipamiento, costo_alquiler))
        connection.commit()
        flash("Equipamiento adquirido con éxito.", "success")
    except Error as e:
        flash(f"Error al adquirir el equipamiento: {e}", "error")
    finally:
        cursor.close()
        connection.close()

    # Redirigir al menú del estudiante después de adquirir el equipamiento
    return redirect(url_for('estudiante.estudiante_menu'))  # Asegúrate de que 'menu_estudiante' sea la ruta correcta

