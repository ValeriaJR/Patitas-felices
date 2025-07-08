from data.db import citas_registradas, pacientes

PACIENTE_NO_ENCONTRADO = "Paciente no encontrado"

def ver_citas():
    print("\n--- Lista de Citas ---")
    
    if not citas_registradas:
        print("📭 No hay citas registradas.")
        return
    
    print("Estado de citas:")
    for cita in citas_registradas:
        paciente = pacientes.get(cita.id_paciente)
        paciente_nombre = paciente.nombre if paciente else PACIENTE_NO_ENCONTRADO
        estado_emoji = {"agendada": "📅", "cancelada": "❌", "realizada": "✅"}
        print(f"{estado_emoji.get(cita.estado, '❓')} {cita}")
        if paciente:
            print(f"   Paciente: {paciente_nombre} ({paciente.especie})")

def cancelar_cita():
    print("\n--- Cancelar Cita ---")
    
    if not citas_registradas:
        print("❌ No hay citas registradas.")
        return
    
    # Mostrar solo citas agendadas
    citas_agendadas = [c for c in citas_registradas if c.estado == "agendada"]
    
    if not citas_agendadas:
        print("❌ No hay citas agendadas para cancelar.")
        return
    
    print("Citas agendadas:")
    for i, cita in enumerate(citas_agendadas, 1):
        paciente = pacientes.get(cita.id_paciente)
        paciente_nombre = paciente.nombre if paciente else PACIENTE_NO_ENCONTRADO
        print(f"{i}. Cita ID: {cita.id} - {paciente_nombre} - {cita.fecha} {cita.hora}")
    
    try:
        seleccion = int(input("Seleccione el número de la cita a cancelar: ")) - 1
        if 0 <= seleccion < len(citas_agendadas):
            cita_a_cancelar = citas_agendadas[seleccion]
        else:
            print("❌ Selección fuera de rango.")
            return
    except ValueError:
        print("❌ Entrada no válida.")
        return
    
    motivo_cancelacion = input("Motivo de cancelación: ")
    
    # Confirmar cancelación
    confirmar = input(f"¿Está seguro de cancelar la cita ID {cita_a_cancelar.id}? (s/n): ").lower()
    
    if confirmar == "s":
        cita_a_cancelar.estado = "cancelada"
        print(f"✅ Cita ID {cita_a_cancelar.id} cancelada exitosamente.")
        print(f"📝 Motivo: {motivo_cancelacion}")
    else:
        print("Cancelación abortada.")

def buscar_citas_por_fecha():
    print("\n--- Buscar Citas por Fecha ---")
    
    if not citas_registradas:
        print("❌ No hay citas registradas.")
        return
    
    fecha_buscar = input("Ingrese la fecha (YYYY-MM-DD): ")
    
    citas_fecha = [c for c in citas_registradas if c.fecha == fecha_buscar]
    
    if not citas_fecha:
        print(f"📭 No se encontraron citas para la fecha {fecha_buscar}.")
        return
    
    print(f"\n📅 Citas para el {fecha_buscar}:")
    for cita in citas_fecha:
        paciente = pacientes.get(cita.id_paciente)
        paciente_nombre = paciente.nombre if paciente else PACIENTE_NO_ENCONTRADO
        estado_emoji = {"agendada": "📅", "cancelada": "❌", "realizada": "✅"}
        print(f"{estado_emoji.get(cita.estado, '❓')} {cita.hora} - {paciente_nombre} - {cita.motivo} - Estado: {cita.estado}") 