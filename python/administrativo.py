from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.security import check_password_hash
from basedatos import connect_to_database
from mysql.connector import Error

# Crea el blueprint
administrativo_blueprint = Blueprint('administrativo', __name__)

def validar_fecha(fecha):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    partes = fecha.split('-')
    if len(partes) == 3:
        año, mes, día = partes
        if len(año) == 4 and año.isdigit() and len(mes) == 2 and mes.isdigit() and len(día) == 2 and día.isdigit():
            return True
    return False

# Función para agregar instructor
from werkzeug.security import generate_password_hash

@administrativo_blueprint.route('/instructor/alta', methods=['POST'])
def alta_instructor():
    # Recopilar datos del formulario
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    ci = request.form.get('ci')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')  # Asegúrate de que este campo esté en el formulario

    connection = connect_to_database()

    try:
        cursor = connection.cursor()

        # Insertar en la tabla `instructores`
        cursor.execute(
            "INSERT INTO instructores (ci, nombre, apellido) VALUES (%s, %s, %s)",
            (ci, nombre, apellido)
        )

        # Insertar en la tabla `login` con el rol de instructor
        cursor.execute(
            "INSERT INTO login (correo, contraseña, rol, ci) VALUES (%s, %s, %s, %s)",
            (correo, contraseña, 'instructor', ci)
        )

        # Confirmar transacciones
        connection.commit()
        flash("Instructor agregado exitosamente.", "success")

    except Error as e:
        connection.rollback()  # Revertir cambios si hay errores
        flash(f"Error al agregar instructor: {e}", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('administrativo.administrativo_menu'))



# Función para eliminar instructor
@administrativo_blueprint.route('/instructor/baja', methods=['POST'])
def baja_instructor():
    ci = request.form.get('ci')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM instructores WHERE ci = %s", (ci,))
        cursor.execute("DELETE FROM login WHERE ci = %s", (ci,))

        connection.commit()
        flash("Instructor eliminado exitosamente.", "success")
    except Error as e:
        flash(f"Error al eliminar instructor: {e}", "error")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrativo.administrativo_menu'))

# Función para modificar instructor
@administrativo_blueprint.route('/instructor/modificar', methods=['POST'])
def modificar_instructor():
    ci = request.form.get('ci')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()

        # Actualizar en la tabla instructores
        cursor.execute(
            "UPDATE instructores SET nombre=%s, apellido=%s WHERE ci=%s",
            (nombre, apellido, ci)
        )

        # Actualizar en la tabla login
        cursor.execute(
            "UPDATE login SET correo=%s, contraseña=%s WHERE ci=%s AND rol='instructor'",
            (correo, contraseña, ci)
        )

        connection.commit()
        flash("Instructor modificado exitosamente.", "success")

    except Error as e:
        connection.rollback()
        flash(f"Error al modificar instructor: {e}", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('administrativo.administrativo_menu'))

@administrativo_blueprint.route('/alumno/alta', methods=['POST'])
def alta_alumno():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    ci = request.form.get('ci')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')  # Asegúrate de que este campo esté en el formulario

    connection = connect_to_database()

    try:
        cursor = connection.cursor()

        # Insertar en la tabla alumnos
        cursor.execute(
            "INSERT INTO alumnos (ci, nombre, apellido, fecha_nacimiento, telefono, correo) VALUES (%s, %s, %s, %s, %s, %s)",
            (ci, nombre, apellido, fecha_nacimiento, telefono, correo)
        )

        # Insertar en la tabla login con rol de 'estudiante'
        cursor.execute(
            "INSERT INTO login (correo, contraseña, rol, ci) VALUES (%s, %s, %s, %s)",
            (correo, contraseña, 'estudiante', ci)
        )

        connection.commit()
        flash("Alumno agregado exitosamente.", "success")

    except Error as e:
        connection.rollback()
        flash(f"Error al agregar alumno: {e}", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('administrativo.administrativo_menu'))

@administrativo_blueprint.route('/alumno/baja', methods=['POST'])
def baja_alumno():
    ci = request.form.get('ci')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM alumnos WHERE ci = %s", (ci,))
        cursor.execute("DELETE FROM login WHERE ci = %s", (ci,))

        connection.commit()
        flash("Alumno eliminado exitosamente.", "success")
    except Error as e:
        flash(f"Error al eliminar alumno: {e}", "error")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrativo.administrativo_menu'))

@administrativo_blueprint.route('/alumno/modificar', methods=['POST'])
def modificar_alumno():
    ci = request.form.get('ci')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    contraseña = request.form.get('contraseña')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()

        # Actualizar en la tabla alumnos
        cursor.execute(
            "UPDATE alumnos SET nombre=%s, apellido=%s, fecha_nacimiento=%s, telefono=%s, correo=%s WHERE ci=%s",
            (nombre, apellido, fecha_nacimiento, telefono, correo, ci)
        )

        # Actualizar en la tabla login
        cursor.execute(
            "UPDATE login SET correo=%s, contraseña=%s WHERE ci=%s AND rol='estudiante'",
            (correo, contraseña, ci)
        )

        connection.commit()
        flash("Estudiante modificado exitosamente.", "success")

    except Error as e:
        connection.rollback()
        flash(f"Error al modificar estudiante: {e}", "error")

    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('administrativo.administrativo_menu'))


@administrativo_blueprint.route('/actividad/modificar', methods=['POST'])
def modificar_actividad():
    actividad_id = request.form.get('actividad_id')
    descripcion = request.form.get('descripcion')
    costo = request.form.get('costo')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE actividades SET descripcion=%s, costo=%s WHERE id=%s",
                       (descripcion, costo, actividad_id))
        connection.commit()
        flash("Instructor modificado exitosamente.", "success")
    except Error as e:
        flash(f"Error al modificar instructor: {e}", "error")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrativo.administrativo_menu'))


@administrativo_blueprint.route('/administrativo/menu', methods=['GET'])
def administrativo_menu():
    return render_template('administrativo_menu.html')