from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from basedatos import connect_to_database
from mysql.connector import Error

# Crea el blueprint
instructor_blueprint = Blueprint('instructor', __name__)

# Ruta para el menú del instructor
@instructor_blueprint.route('/instructor/menu', methods=['GET'])
def instructor_menu():
    return render_template('instructor_menu.html')

# Ruta para registrar información del instructor
@instructor_blueprint.route('/instructor/registrar', methods=['POST'])
def registrar_instructor_route():
    data = request.form
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    if not validar_cedula(ci):
        flash("La cédula debe tener exactamente 8 dígitos numéricos.")
        return redirect(url_for('instructor.instructor_menu'))

    message = registrar_instructor(ci, nombre, apellido)
    flash(message)
    return redirect(url_for('instructor.instructor_menu'))

# Ruta para eliminar instructor
@instructor_blueprint.route('/instructor/eliminar', methods=['POST'])
def eliminar_instructor_route():
    data = request.form
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')

    success = eliminar_instructor(ci, nombre, apellido)
    if success:
        flash("Instructor eliminado exitosamente.")
    else:
        flash("No se encontró el instructor.")
    
    return redirect(url_for('instructor.instructor_menu'))

# Ruta para anotarse a una clase
@instructor_blueprint.route('/instructor/anotarse', methods=['POST'])
def anotarse_clase():
    # Falta implementar logica !!
    flash("Anotado a la clase exitosamente.") 
    return redirect(url_for('instructor.instructor_menu'))
