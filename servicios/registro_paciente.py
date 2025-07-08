import random
from modelos.paciente import Paciente
from data.db import pacientes, propietarios
from servicios.registro_propietario import registrar_propietario  # para redirigir si no existe

def generar_id_unico_paciente():
    while True:
        nuevo_id = str(random.randint(10000, 99999))
        if nuevo_id not in pacientes:
            return nuevo_id

def registrar_paciente():
    print("\n--- Registro de Paciente ---")
    id_propietario = input("Ingrese el ID del Propietario: ")

    if id_propietario not in propietarios:
        print("❌ No existe un propietario con ese ID.")
        opcion = input("¿Desea registrarlo ahora? (s/n): ").lower()
        if opcion == "s":
            registrar_propietario()
            id_propietario = input("Ingrese nuevamente el ID del Propietario registrado: ")
            if id_propietario not in propietarios:
                print("❌ Error: El propietario aún no existe. Cancelando registro de paciente.")
                return
        else:
            print("Registro de paciente cancelado.")
            return

    while True:
        nombre = input("Nombre del paciente: ")
        edad = input("Edad: ")
        especie = input("Especie (Perro/Gato): ")
        raza = input("Raza: ")
        peso = input("Peso (kg): ")
        sexo = input("Sexo (Macho/Hembra): ")

        id_paciente = generar_id_unico_paciente()
        paciente = Paciente(id_paciente, nombre, edad, especie, raza, peso, sexo, id_propietario)
        pacientes[id_paciente] = paciente
        propietarios[id_propietario].mascotas.append(id_paciente)

        print(f"✅ Paciente registrado con éxito. ID generado: {id_paciente}")
        print("ℹ️ Para ver tus pacientes registrados, puedes marcar la opción 6 en el menú principal.")


        otra = input("¿Desea registrar otra mascota para este propietario? (s/n): ").lower()
        if otra != "s":
            break


def ver_mascotas_por_propietario():
    print("\n--- Ver Mascotas por Propietario ---")
    id_propietario = input("Ingrese el ID del propietario: ")

    if id_propietario not in propietarios:
        print("❌ No existe un propietario con ese ID.")
        return

    mascota_ids = propietarios[id_propietario].mascotas
    if not mascota_ids:
        print("📭 Este propietario no tiene mascotas registradas.")
        return

    print(f"🐾 Mascotas registradas para {propietarios[id_propietario].nombre}:")
    for id_mascota in mascota_ids:
        mascota = pacientes.get(id_mascota)
        if mascota:
            print(f" - {mascota.nombre} ({mascota.especie}, {mascota.raza}, {mascota.sexo}, {mascota.edad} años, {mascota.peso}kg)")
