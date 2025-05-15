from modelos.cita import Cita
from modelos.cita import Cita
from data.db import citas_registradas
import random


# Lista para almacenar citas 
citas_registradas = []

#llamo los vets disponibles

def cargar_veterinarios():
    try:
        with open("data/veterinarios.txt", "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("⚠️ Archivo de veterinarios no encontrado.")
        return []

#genero aleatoriamente un id para la cita [un radicado]
def generar_id_unico_cita():
    while True:
        nuevo_id = str(random.randint(1000, 9999))
        if not any(cita.id == nuevo_id for cita in citas_registradas):
            return nuevo_id

def registrar_cita(fecha, hora, motivo, id_paciente, id_veterinario):
    id = generar_id_unico_cita()
    nueva_cita = Cita(id, fecha, hora, motivo, id_paciente, id_veterinario)
    citas_registradas.append(nueva_cita)
    print(f"✅ Cita registrada exitosamente con ID: {id}")


from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente
from data.db import propietarios, pacientes

def agendar_cita_completa():
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
        veterinarios_dict = []
        for idx, vet_line in enumerate(veterinarios, 1):
            partes = vet_line.split(",")
            if len(partes) >= 2:
                vet_id, vet_nombre = partes[0], partes[1]
                veterinarios_dict.append({"id": vet_id, "nombre": vet_nombre})
                print(f"{idx}. {vet_nombre} (ID: {vet_id})")

        while True:
            try:
                seleccion_vet = int(input("Seleccione el número correspondiente al veterinario: "))
                if 1 <= seleccion_vet <= len(veterinarios_dict):
                    break
                else:
                    print("⚠️ Selección fuera de rango. Intente de nuevo.")
            except ValueError:
                print("⚠️ Entrada no válida. Ingrese un número.")

        id_veterinario = veterinarios_dict[seleccion_vet - 1]["id"]
        registrar_cita(fecha, hora, motivo, paciente_seleccionado.id, id_veterinario)
