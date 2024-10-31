import mysql.connector

# Conexión a la base de datos
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="proyectoFinal"
)

cursor = db_connection.cursor()