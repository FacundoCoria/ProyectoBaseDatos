import mysql.connector
from mysql.connector import Error

# Realiza la conexion con la base de datos
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
