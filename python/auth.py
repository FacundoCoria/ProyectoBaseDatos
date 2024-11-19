from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from basedatos import connect_to_database
from mysql.connector import Error

auth_blueprint = Blueprint('auth', __name__)

# Función para registrar a un usuario con un correo
def register_user(correo, contraseña, rol, ci):
    connection = connect_to_database()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "INSERT INTO login (correo, contraseña, rol, ci) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (correo, contraseña, rol, ci))
        connection.commit()
        print("Usuario registrado exitosamente.")
        return True
    except Error as e:
        print(f"Error al registrar el usuario: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# Función para autenticar usuario
def authenticate_user(correo, contraseña):
    connection = connect_to_database()
    if connection is None:
        return None, None
    try:
        cursor = connection.cursor()
        query = "SELECT ci, rol FROM login WHERE correo = %s AND contraseña = %s"
        cursor.execute(query, (correo, contraseña))
        result = cursor.fetchone()
        return (result[0], result[1]) if result else (None, None)
    except Error as e:
        print(f"Error en la autenticación: {e}")
        return None, None
    finally:
        cursor.close()
        connection.close()

# Nueva función para registrar al instructor
def register_instructor(ci, nombre, apellido):
    connection = connect_to_database()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = "INSERT INTO instructores (ci, nombre, apellido) VALUES (%s, %s, %s)"
        cursor.execute(query, (ci, nombre, apellido))
        connection.commit()
        print("Instructor registrado exitosamente.")
        return True
    except Error as e:
        print(f"Error al registrar el instructor: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# Nueva función para registrar al alumno
def register_alumno(ci, nombre, apellido, fecha_nacimiento, telefono, correo):
    connection = connect_to_database()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO alumnos (ci, nombre, apellido, fecha_nacimiento, telefono, correo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (ci, nombre, apellido, fecha_nacimiento, telefono, correo))
        connection.commit()
        print("Alumno registrado exitosamente.")
        return True
    except Error as e:
        print(f"Error al registrar el alumno: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

@auth_blueprint.route('/registerInstructor', methods=['GET', 'POST'])
def registerInstructor():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        ci = request.form.get('ci')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        rol = "instructor"  # Define el rol aquí

        # Primero registra el usuario en la tabla login
        if register_user(correo, contraseña, rol, ci):
            # Luego registra los datos específicos en la tabla instructores
            if register_instructor(ci, nombre, apellido):
                flash('Instructor registrado exitosamente.')
                return redirect(url_for('auth.login'))
            else:
                flash('Error al registrar al instructor.')
        else:
            flash('Error al registrar el usuario.')

    return render_template('registerInstructor.html')

@auth_blueprint.route('/registerEstudiante', methods=['GET', 'POST'])
def registerEstudiante():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        ci = request.form.get('ci')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        telefono = request.form.get('telefono')
        rol = "estudiante"  # Define el rol aquí

        # Primero registra el usuario en la tabla login
        if register_user(correo, contraseña, rol, ci):
            # Luego registra los datos específicos en la tabla alumnos
            if register_alumno(ci, nombre, apellido, fecha_nacimiento, telefono, correo):
                flash('Estudiante registrado exitosamente.')
                return redirect(url_for('auth.login'))
            else:
                flash('Error al registrar al estudiante.')
        else:
            flash('Error al registrar el usuario.')

    return render_template('registerEstudiante.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        ci, rol = authenticate_user(correo, contraseña)
        if ci:
            connection = connect_to_database()
            try:
                cursor = connection.cursor()
                nombre = "Admin" 
                
                if rol == "instructor":
                    cursor.execute("SELECT nombre FROM instructores WHERE ci = %s", (ci,))
                    nombre_result = cursor.fetchone()
                    nombre = nombre_result[0] if nombre_result else nombre
                elif rol == "estudiante":
                    cursor.execute("SELECT nombre FROM alumnos WHERE ci = %s", (ci,))
                    nombre_result = cursor.fetchone()
                    nombre = nombre_result[0] if nombre_result else nombre

                cursor.close()
                connection.close()

                flash('Inicio de sesión exitoso.')
                if rol == "instructor":
                    return render_template('instructor_menu.html', nombre=nombre)
                elif rol == "estudiante":
                    return render_template('estudiante_menu.html', nombre=nombre)
                elif rol == "administrador":
                    return render_template('administrativo_menu.html', nombre=nombre)
            except Error as e:
                print(f"Error al obtener el nombre: {e}")
                flash('Error al iniciar sesión.')
                return redirect(url_for('auth.login'))
        else:
            flash('Correo o contraseña incorrectos.')

    return render_template('login.html')

