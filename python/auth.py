from flask import Blueprint, render_template, request, redirect, url_for, flash
from basedatos import connect_to_database
from mysql.connector import Error

auth_blueprint = Blueprint('auth', __name__)

# Funcion para registrar a un usuario con un correo.

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

# Funcion para poder iniciar sesion con un usuario.

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

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        rol = request.form.get('rol')
        ci = request.form.get('ci')
        if register_user(correo, contraseña, rol, ci):
            flash('Usuario registrado exitosamente.')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al registrar el usuario.')

    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        ci, rol = authenticate_user(correo, contraseña)
        if ci:
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('instructor.instructor_menu'))  # Redirige al menú del instructor
        else:
            flash('Correo o contraseña incorrectos.')

    return render_template('login.html')
