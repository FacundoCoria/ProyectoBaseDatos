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
@administrativo_blueprint.route('/instructor/alta', methods=['POST'])
def alta_instructor():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    ci = request.form.get('ci')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO instructores (nombre, apellido, ci) VALUES (%s, %s, %s)",
                       (nombre, apellido, ci))
        connection.commit()
        flash("Instructor agregado exitosamente.", "success")
    except Error as e:
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
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE instructores SET nombre=%s, apellido=%s WHERE ci=%s",
                       (nombre, apellido, ci))
        connection.commit()
        flash("Instructor modificado exitosamente.", "success")
    except Error as e:
        flash(f"Error al modificar instructor: {e}", "error")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('administrativo.administrativo_menu'))

# Funciones similares para alumnos, turnos, y actividades
@administrativo_blueprint.route('/alumno/alta', methods=['POST'])
def alta_alumno():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    ci = request.form.get('ci')
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    telefono = request.form.get('telefono')
    correo = request.form.get('correo')
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO alumnos (nombre, apellido, ci, fecha_nacimiento, telefono, correo) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nombre, apellido, ci, fecha_nacimiento, telefono, correo))
        connection.commit()
        flash("Alumno agregado exitosamente.", "success")
    except Error as e:
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
    connection = connect_to_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE alumnos SET nombre=%s, apellido=%s, fecha_nacimiento=%s, correo=%s, telefono=%s WHERE ci=%s",
                       (nombre, apellido, fecha_nacimiento, correo, telefono, ci))
        connection.commit()
        flash("Estudiante modificado exitosamente.", "success")
    except Error as e:
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