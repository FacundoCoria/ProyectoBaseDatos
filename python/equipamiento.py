from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from basedatos import connect_to_database
from mysql.connector import Error

equipamiento_blueprint = Blueprint('equipamiento', __name__)

@equipamiento_blueprint.route('/equipamiento/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno_clase_route():
    connection = connect_to_database()
    if request.method == 'POST':
        data = request.form
        id_clase = data.get('id_clase')
        ci_alumno = data.get('ci_alumno')
        id_equipamiento = data.get('id_equipamiento', None)
        es_alquilado = data.get('es_alquilado') == 'on'

        if not id_clase or not ci_alumno:
            flash("Debe proporcionar id_clase y ci_alumno.", "error")
            return redirect(url_for('equipamiento.registrar_alumno_clase_route'))

        try:
            # Consulta para obtener el costo del equipamiento si es alquilado
            costo_alquiler = 0.0
            if es_alquilado and id_equipamiento:
                cursor = connection.cursor()
                query = "SELECT costo FROM equipamiento WHERE id = %s"
                cursor.execute(query, (id_equipamiento,))
                resultado = cursor.fetchone()
                if resultado:
                    costo_alquiler = resultado[0]

            # Insertar el registro en la tabla alumno_clase
            query = """
                INSERT INTO alumno_clase (id_clase, ci_alumno, id_equipamiento, costo_adicional)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (id_clase, ci_alumno, id_equipamiento, costo_alquiler if es_alquilado else 0.0))
            connection.commit()
            flash("Alumno registrado exitosamente en la clase.", "success")
        except Error as e:
            flash(f"Error al registrar al alumno en la clase: {e}", "error")
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('equipamiento.registrar_alumno_clase_route'))
    
    # Obtener el listado de clases y equipamientos para mostrar en el formulario
    cursor = connection.cursor()
    cursor.execute("SELECT id, descripcion FROM equipamiento")
    equipamientos = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template('registrar_alumno_clase.html', equipamientos=equipamientos)
