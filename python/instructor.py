from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from basedatos import connect_to_database
from mysql.connector import Error

# Crea el blueprint
instructor_blueprint = Blueprint('instructor', __name__)

def validar_cedula(ci):
    """ Valida que la cédula tenga exactamente 8 dígitos y sea numérica. """
    return len(ci) == 8 and ci.isdigit()

def eliminar_instructor(ci, nombre, apellido):
    connection = connect_to_database()
    if connection is None:
        return False  # Retorna False si no se pudo conectar

    try:
        cursor = connection.cursor()
        query = "DELETE FROM instructores WHERE ci = %s AND nombre = %s AND apellido = %s"
        cursor.execute(query, (ci, nombre, apellido))
        connection.commit()
        
        return cursor.rowcount > 0  # Retorna True si se eliminó exitosamente
    except Error as e:
        return False  # Retorna False en caso de error
    finally:
        cursor.close()
        connection.close()

# Ruta para el menú del instructor
@instructor_blueprint.route('/instructor/menu', methods=['GET'])
def instructor_menu():
    return render_template('instructor_menu.html')
# Ruta para eliminar instructor
@instructor_blueprint.route('/instructor/eliminar', methods=['POST'])
def eliminar_instructor_route():
    data = request.form
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    success = eliminar_instructor(ci, nombre, apellido)
    if success:
        return jsonify({'message': "Instructor eliminado exitosamente."}), 
    else:
        return jsonify({'error': "No se encontró el instructor."}), 400

# Ruta para anotarse a una clase
@instructor_blueprint.route('/instructor/anotarse', methods=['POST'])
def anotarse_clase():
    # Implementa lógica para anotarse a una clase
    flash("Anotado a la clase exitosamente.") 
    return redirect(url_for('instructor.instructor_menu'))
