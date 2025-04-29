from modelos.paciente import Paciente
from data.db import pacientes, propietarios

def registrar_paciente():
    print("\n--- Registro de Paciente ---")
    id_paciente = input("ID del Paciente: ")
    if id_paciente in pacientes:
        print("❌ Ya existe un paciente con ese ID.")
        return
    nombre = input("Nombre: ")
    edad = input("Edad: ")
    especie = input("Especie (Perro/Gato): ")
    raza = input("Raza: ")
    peso = input("Peso (kg): ")
    sexo = input("Sexo (Macho/Hembra): ")
    id_propietario = input("ID del Propietario: ")

    if id_propietario not in propietarios:
        print("❌ Error: No existe un propietario con ese ID. Regístrelo primero.")
        return

    paciente = Paciente(id_paciente, nombre, edad, especie, raza, peso, sexo, id_propietario)
    pacientes[id_paciente] = paciente
    propietarios[id_propietario].mascotas.append(id_paciente)
    print("✅ Paciente registrado con éxito.")