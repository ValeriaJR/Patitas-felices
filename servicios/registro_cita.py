from modelos.cita import Cita
from data.db import citas_registradas
import random

# Lista para almacenar citas 
citas_registradas = []

#llamo los vets disponibles

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

#genero aleatoriamente un id para la cita [un radicado]
def generar_id_unico_cita():
    while True:
        nuevo_id = str(random.randint(1000, 9999))
        if not any(cita.id == nuevo_id for cita in citas_registradas):
            return nuevo_id

def registrar_cita(fecha, hora, motivo, id_paciente, id_veterinario):
    cita_id = generar_id_unico_cita()
    nueva_cita = Cita(cita_id, fecha, hora, motivo, id_paciente, id_veterinario)
    citas_registradas.append(nueva_cita)
    print(f"✅ Cita registrada exitosamente con ID: {cita_id}")


