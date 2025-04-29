from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente
from data.db import propietarios, pacientes


def mostrar_propietarios():
    print("\n--- Lista de Propietarios ---")
    for p in propietarios.values():
        print(p)

def mostrar_pacientes():
    print("\n--- Lista de Pacientes ---")
    for p in pacientes.values():
        print(p)

def menu():
    while True:
        print("\n===== Menú Principal - Veterinaria =====")
        print("1. Registrar propietario")
        print("2. Registrar paciente")
        print("3. Ver propietarios")
        print("4. Ver pacientes")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_propietario()
        elif opcion == "2":
            registrar_paciente()
        elif opcion == "3":
            mostrar_propietarios()
        elif opcion == "4":
            mostrar_pacientes()
        elif opcion == "0":
            print("Hasta luego 🐾")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()