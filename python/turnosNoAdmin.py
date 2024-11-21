from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from basedatos import connect_to_database

# Crear el blueprint para turno
turnosNoAdmin_blueprint = Blueprint('turnosNoAdmin', __name__)

# Ruta para listar los turnos con clase e instructor
@turnosNoAdmin_blueprint.route('/turnosNoAdmin/listar', methods=['GET'])
def mostrar_turnos():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT clase.id, turnos.hora_inicio, turnos.hora_fin FROM clase JOIN turnos ON clase.id_turno = turnos.id WHERE clase.id_actividad = 2;")
        turnos = cursor.fetchall()
    except Exception as e:
        flash("Error al listar los turnos: {}".format(e))
        turnos = []
    finally:
        cursor.close()
        conn.close()
    
    return render_template('mostrar_turnos.html', turnos=turnos)