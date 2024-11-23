def unirse_clase():
    connection = connect_to_database()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO alumno_clase (ci, nombre, apellido, fecha_nacimiento, telefono, correo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (ci, nombre, apellido, fecha_nacimiento, telefono, correo))
        connection.commit()
        print("Te has unido exitosamente.")
        return True
    except Error as e:
        print(f"Error al inscibirse: {e}")
        return False
    finally:
        cursor.close()
        connection.close()