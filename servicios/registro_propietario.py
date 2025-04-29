from modelos.propietario import Propietario
from data.db import propietarios

def registrar_propietario():
    print("\n--- Registro de Propietario ---")
    id_propietario = input("ID del Propietario: ")
    if id_propietario in propietarios:
        print("❌ Ya existe un propietario con ese ID.")
        return
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    correo = input("Correo electrónico: ")
    direccion = input("Dirección: ")

    propietario = Propietario(id_propietario, nombre, telefono, correo, direccion)
    propietarios[id_propietario] = propietario
    print("✅ Propietario registrado con éxito.")
