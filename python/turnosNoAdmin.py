from flask import Blueprint, request, render_template, flash, redirect, url_for
from basedatos import connect_to_database

# Crear el blueprint para turnos
turnosNoAdmin_blueprint = Blueprint('turnosNoAdmin', __name__)

# Ruta para listar los turnos con clase e instructor
@turnosNoAdmin_blueprint.route('/turnosNoAdmin/listar', methods=['GET'])
def mostrar_turnos():
    id_clase = request.args.get('id')
    print(id_clase)
    
    conn = connect_to_database()
    cursor = conn.cursor()
    
    try:
        query = ("SELECT clase.id, turnos.hora_inicio, turnos.hora_fin FROM clase JOIN turnos ON clase.id_turno = turnos.id WHERE clase.id_actividad = %s")
        cursor.execute(query,(id_clase,))
        turnos = cursor.fetchall()
    except Exception as e:
        flash("Error al listar los turnos: {}".format(e))
        turnos = []
    finally:
        cursor.close()
        conn.close()

    return render_template('mostrar_turnos.html', turnos=turnos)
