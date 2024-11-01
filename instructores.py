from login import connect_to_database
from mysql.connector import Error

def registrar_instructor(ci, nombre, apellido):
    connection = connect_to_database()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return

    try:
        cursor = connection.cursor()
        query = "INSERT INTO instructores (ci, nombre, apellido) VALUES (%s, %s, %s)"
        cursor.execute(query, (ci, nombre, apellido))
        connection.commit()
        print("Instructor registrado exitosamente.")
    except Error as e:
        print(f"Error al registrar el instructor: {e}")
    finally:
        cursor.close()
        connection.close()

def eliminar_instructor(ci, nombre, apellido):
    connection = connect_to_database()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos.")
        return False  # Retorna False si no se pudo conectar

    try:
        cursor = connection.cursor()
        query = "DELETE FROM instructores WHERE ci = %s AND nombre = %s AND apellido = %s"
        cursor.execute(query, (ci, nombre, apellido))
        connection.commit()
        
        if cursor.rowcount > 0:
            return True  # Se eliminó exitosamente
        else:
            return False  # No se encontró el instructor
    except Error as e:
        print(f"Error al eliminar el instructor: {e}")
        return False  # Retorna False en caso de error
    finally:
        cursor.close()
        connection.close()
