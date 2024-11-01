import mysql.connector
from mysql.connector import Error
from getpass import getpass

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='rootpassword',
            database='proyectoFinal'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def registrar_usuario(correo, contraseña, rol, ci):
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

def autenticar_usuario(correo, contraseña):
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
