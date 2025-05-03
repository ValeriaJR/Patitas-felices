from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente
from servicios.registro_cita import registrar_cita
from servicios.registro_paciente import registrar_paciente, ver_mascotas_por_propietario
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
            print("\n--- Agendar Cita Médica ---")

            id_propietario = input("Ingrese el ID del propietario: ")

            if id_propietario not in propietarios:
                print("Propietario no encontrado. Por favor regístrelo primero.")
                registrar_propietario()
                registrar_paciente()
            else:
                # Buscar pacientes del propietario
                mascotas = [p for p in pacientes.values() if p.id_propietario == id_propietario]
                if not mascotas:
                    print("Este propietario no tiene pacientes registrados. Registremos uno.")
                    registrar_paciente()
                    mascotas = [p for p in pacientes.values() if p.id_propietario == id_propietario]

                if len(mascotas) == 1:
                    paciente_seleccionado = mascotas[0]
                else:
                    print("¿Para cuál paciente es la cita?")
                    for idx, m in enumerate(mascotas, 1):
                        print(f"{idx}. {m.nombre}")
                    seleccion = int(input("Seleccione el número correspondiente: "))
                    paciente_seleccionado = mascotas[seleccion - 1]

                fecha = input("Fecha (YYYY-MM-DD): ")
                hora = input("Hora (HH:MM): ")
                motivo = input("Motivo: ")

                # Cargar y seleccionar veterinario
                veterinarios = cargar_veterinarios()
                if not veterinarios:
                    print("❌ No hay veterinarios disponibles.")
                    return

                print("Veterinarios disponibles:")
                for idx, vet in enumerate(veterinarios, 1):
                    print(f"{idx}. {vet['nombre']} (ID: {vet['id']})")

                while True:
                    try:
                        seleccion_vet = int(input("Seleccione el número correspondiente al veterinario: "))
                        if 1 <= seleccion_vet <= len(veterinarios):
                            break
                        else:
                            print("⚠️ Selección fuera de rango. Intente de nuevo.")
                    except ValueError:
                        print("⚠️ Entrada no válida. Ingrese un número.")

                id_veterinario = veterinarios[seleccion_vet - 1]["id"]
                registrar_cita(fecha, hora, motivo, paciente_seleccionado.id, id_veterinario)

        elif opcion == "6":
            ver_mascotas_por_propietario()

        elif opcion == "0":
            print("Hasta luego 🐾")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
