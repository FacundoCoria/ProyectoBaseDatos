# clase.py
from flask import Blueprint, request, render_template, flash, redirect, url_for
from basedatos import connect_to_database

# Crear el blueprint para clase
clase_blueprint = Blueprint('clase', __name__)

# Ruta para mostrar el formulario de alta de clase
@clase_blueprint.route('/clase/alta', methods=['GET'])
def alta_clase_form():
    return render_template('alta_clase.html')

# Ruta para dar de alta una nueva clase
@clase_blueprint.route('/clase/alta', methods=['POST'])
def alta_clase():
    # Recibir los datos del formulario
    ci_instructor = request.form.get('ci_instructor')
    id_actividad = request.form.get('id_actividad')
    id_turno = request.form.get('id_turno')
    tipo_clase = request.form.get('tipo_clase')

    # Conectar a la base de datos y realizar la inserción
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Verificar que el instructor, la actividad y el turno existen antes de registrar la clase
        cursor.execute("SELECT ci FROM instructores WHERE ci = %s", (ci_instructor,))
        instructor = cursor.fetchone()
        cursor.execute("SELECT id FROM actividades WHERE id = %s", (id_actividad,))
        actividad = cursor.fetchone()
        cursor.execute("SELECT id FROM turnos WHERE id = %s", (id_turno,))
        turno = cursor.fetchone()

        if not instructor:
            flash("El instructor con CI {} no existe.".format(ci_instructor))
        elif not actividad:
            flash("La actividad con ID {} no existe.".format(id_actividad))
        elif not turno:
            flash("El turno con ID {} no existe.".format(id_turno))
        else:
            # Registrar la clase en la base de datos
            cursor.execute("""
                INSERT INTO clase (ci_instructor, id_actividad, id_turno, dictada, tipo_clase) 
                VALUES (%s, %s, %s, 0, %s)  -- 0 para indicar que no ha sido dictada
            """, (ci_instructor, id_actividad, id_turno, tipo_clase ))
            conn.commit()
            flash("Clase registrada exitosamente.")
    except Exception as e:
        flash("Ocurrió un error al registrar la clase: {}".format(e))
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('clase.alta_clase_form'))
