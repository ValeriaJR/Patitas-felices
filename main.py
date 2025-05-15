from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente
from servicios.registro_cita import registrar_cita
from servicios.registro_paciente import registrar_paciente, ver_mascotas_por_propietario
from servicios.registro_cita import agendar_cita_completa
from data.db import propietarios, pacientes


def mostrar_propietarios():
    print("\n--- Lista de Propietarios ---")
    for p in propietarios.values():
        print(p)


def mostrar_pacientes():
    print("\n--- Lista de Pacientes ---")
    
    for p in pacientes.values():
        print(p)


def cargar_veterinarios():
    try:
        with open("data/veterinarios.txt", "r", encoding="utf-8") as file:
            veterinarios = []
            for linea in file:
                partes = linea.strip().split(",")
                if len(partes) >= 2:
                    veterinarios.append({"id": partes[0], "nombre": partes[1]})
            return veterinarios
    except FileNotFoundError:
        print("⚠️ Archivo de veterinarios no encontrado.")
        return []


def menu():
    while True:
        print("\n===== Menú Principal - Veterinaria =====")
        print("1. Registrar propietario")
        print("2. Registrar paciente")
        print("3. Ver propietarios")
        print("4. Ver pacientes")
        print("5. Registrar cita médica")
        print("6. Ver mascotas de un propietario")
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
        elif opcion == "5":
            agendar_cita_completa()
        elif opcion == "6":
            ver_mascotas_por_propietario()

        elif opcion == "0":
            print("Hasta luego 🐾")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
