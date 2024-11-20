from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from basedatos import connect_to_database

# Crear el blueprint 
clasesNoAdmin_blueprint = Blueprint('clasesNoAdmin', __name__)

# Ruta para listar los turnos de una clase
@clasesNoAdmin_blueprint.route('/clasesNoAdmin/listar', methods=['GET'])
def mostrar_clases():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT tipo_clase FROM clase")
        clases = cursor.fetchall()
    except Exception as e:
        flash("Error al listar los turnos: {}".format(e))
        clases = []
    finally:
        cursor.close()
        conn.close()

    return render_template('mostrar_clases.html', clases=clases)