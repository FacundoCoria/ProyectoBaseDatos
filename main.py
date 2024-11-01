from login import autenticar_usuario, registrar_usuario
from instructores import registrar_instructor, eliminar_instructor
import getpass

def validar_cedula(ci):
    """ Valida que la cédula tenga exactamente 8 dígitos y sea numérica. """
    if len(ci) == 8 and ci.isdigit():
        return True
    return False

def main():
    print("=== Sistema de Gestión ===")
    ci_autenticado, rol = None, None
    while True:
        print("\n1. Iniciar sesión")
        print("2. Registrar nuevo usuario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            correo = input("Ingrese su correo: ")
            contraseña = getpass.getpass("Ingrese su contraseña: ")
            ci_autenticado, rol = autenticar_usuario(correo, contraseña)
            if rol:
                print(f"Bienvenido, {rol.capitalize()}.")
                if rol == "instructor":
                    manejar_instructor(ci_autenticado)  # Manejar las opciones del instructor
            else:
                print("Error: Autenticación fallida.")
        elif opcion == "2":
            correo = input("Ingrese su correo: ")
            contraseña = getpass.getpass("Ingrese su contraseña: ")
            rol = input("Ingrese el rol (administrador, instructor, estudiante): ").lower()
            ci = input("Ingrese su cédula: ")
            if not validar_cedula(ci):
                print("Error: La cédula debe tener exactamente 8 dígitos y ser numérica.")
                continue  # Volver al menú principal si la cédula es inválida

            if rol in ["administrador", "instructor", "estudiante"]:
                if registrar_usuario(correo, contraseña, rol, ci):
                    print("Registro exitoso. Ahora puede iniciar sesión.")
            else:
                print("Rol no válido. Intente nuevamente.")
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

def manejar_instructor(ci_autenticado):
    print("Bienvenido, Instructor.")
    while True:
        print("\n1. Registrar mi información")
        print("2. Eliminar mi información")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            if nombre and apellido:
                registrar_instructor(ci_autenticado, nombre, apellido)
            else:
                print("Error: Datos incompletos.")
        elif opcion == "2":
            ci = input("Ingrese su cédula: ")
            if not validar_cedula(ci):
                print("Error: La cédula debe tener exactamente 8 dígitos y ser numérica.")
                continue  # Volver al menú del instructor si la cédula es inválida

            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            if eliminar_instructor(ci, nombre, apellido):  
                print("Instructor eliminado exitosamente.")
        elif opcion == "3":
            print("Unirse a una clase")
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
