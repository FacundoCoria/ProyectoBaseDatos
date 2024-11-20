from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from basedatos import connect_to_database

# Crear el blueprint para turno
turnoNoAdmin_blueprint = Blueprint('turnoNoAdmin', __name__)

# Ruta para listar los turnos con clase e instructor
@turnoNoAdmin_blueprint.route('/turnoNoAdmin/listar', methods=['GET'])
def mostrar_turnos():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM turnos")
        turnos = cursor.fetchall()
    except Exception as e:
        flash("Error al listar los turnos: {}".format(e))
        turnos = []
    finally:
        cursor.close()
        conn.close()

    user_type = session.get('user_type', 'estudiante')  # Valor por defecto 'estudiante'

    return render_template('mostrar_turnos.html', turnos=turnos, user_type=user_type)
