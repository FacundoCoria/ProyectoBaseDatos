from flask import Blueprint, request, render_template, flash, redirect, url_for
from basedatos import connect_to_database

# Crear el blueprint para turno
turno_blueprint = Blueprint('turno', __name__)

# Ruta para mostrar el formulario de alta de turno
@turno_blueprint.route('/turno/alta', methods=['GET'])
def alta_turno_form():
    return render_template('alta_turno.html')

# Ruta para dar de alta un nuevo turno
@turno_blueprint.route('/turno/alta', methods=['POST'])
def alta_turno():
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO turnos (hora_inicio, hora_fin) VALUES (%s, %s)", (hora_inicio, hora_fin))
        conn.commit()
        flash("Turno registrado exitosamente.")
    except Exception as e:
        flash("Error al registrar el turno: {}".format(e))
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('turno.listar_turnos'))

# Ruta para listar los turnos
@turno_blueprint.route('/turno/listar', methods=['GET'])
def listar_turnos():
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

    return render_template('listar_turnos.html', turnos=turnos)

# Ruta para eliminar un turno
@turno_blueprint.route('/turno/eliminar/<int:id_turno>', methods=['POST'])
def eliminar_turno(id_turno):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM turnos WHERE id = %s", (id_turno,))
        conn.commit()
        flash("Turno eliminado exitosamente.")
    except Exception as e:
        flash("Error al eliminar el turno: {}".format(e))
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('turno.listar_turnos'))

# Ruta para mostrar el formulario de modificación de turno
@turno_blueprint.route('/turno/modificar/<int:id_turno>', methods=['GET'])
def modificar_turno_form(id_turno):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM turnos WHERE id = %s", (id_turno,))
        turno = cursor.fetchone()
    except Exception as e:
        flash("Error al cargar el turno: {}".format(e))
        turno = None
    finally:
        cursor.close()
        conn.close()

    return render_template('modificar_turno.html', turno=turno)

# Ruta para modificar un turno
@turno_blueprint.route('/turno/modificar/<int:id_turno>', methods=['POST'])
def modificar_turno(id_turno):
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')

    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE turnos SET hora_inicio = %s, hora_fin = %s WHERE id = %s", (hora_inicio, hora_fin, id_turno))
        conn.commit()
        flash("Turno modificado exitosamente.")
    except Exception as e:
        flash("Error al modificar el turno: {}".format(e))
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('turno.listar_turnos'))
