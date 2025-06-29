from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente, ver_mascotas_por_propietario
from servicios.registro_cita import registrar_cita
from servicios.gestion_citas import ver_citas, cancelar_cita, buscar_citas_por_fecha
from servicios.historia_clinica import crear_historia_clinica, consultar_historial_paciente, registrar_atencion_medica
from servicios.inventario_medicamentos import registrar_medicamento, actualizar_stock, mostrar_inventario, verificar_alertas_inventario
from servicios.editar_datos import menu_editar_datos
from servicios.informes import generar_informe_mensual
from data.db import propietarios, pacientes, citas_registradas

MENU_VOLVER_PRINCIPAL = "0. Volver al menú principal"
PROMPT_SELECCIONE_OPCION = "Seleccione una opción: "
MSG_OPCION_INVALIDA = "❌ Opción inválida. Intente de nuevo."

def mostrar_propietarios():
    print("\n--- Lista de Propietarios ---")
    if not propietarios:
        print("📭 No hay propietarios registrados.")
        return
    for p in propietarios.values():
        print(p)


def mostrar_pacientes():
    print("\n--- Lista de Pacientes ---")
    if not pacientes:
        print("📭 No hay pacientes registrados.")
        return
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


def submenu_citas():
    while True:
        print("\n=== Gestión de Citas ===")
        print("1. Registrar nueva cita")
        print("2. Ver todas las citas")
        print("3. Cancelar cita")
        print("4. Buscar citas por fecha")
        print("5. Registrar atención médica")
        print(MENU_VOLVER_PRINCIPAL)
        opcion = input(PROMPT_SELECCIONE_OPCION)
        
        if opcion == "1":
            agendar_cita_mejorada()
        elif opcion == "2":
            ver_citas()
        elif opcion == "3":
            cancelar_cita()
        elif opcion == "4":
            buscar_citas_por_fecha()
        elif opcion == "5":
            registrar_atencion_medica()
        elif opcion == "0":
            break
        else:
            print(MSG_OPCION_INVALIDA)


def submenu_historia_clinica():
    while True:
        print("\n=== Historia Clínica ===")
        print("1. Crear historia clínica")
        print("2. Consultar historial de paciente")
        print(MENU_VOLVER_PRINCIPAL)
        opcion = input(PROMPT_SELECCIONE_OPCION)
        
        if opcion == "1":
            crear_historia_clinica()
        elif opcion == "2":
            consultar_historial_paciente()
        elif opcion == "0":
            break
        else:
            print(MSG_OPCION_INVALIDA)


def submenu_inventario():
    while True:
        print("\n=== Inventario de Medicamentos ===")
        print("1. Registrar medicamento")
        print("2. Actualizar stock")
        print("3. Ver inventario")
        print("4. Verificar alertas")
        print("0. Volver al menú principal")
        opcion = input(PROMPT_SELECCIONE_OPCION)
        
        if opcion == "1":
            registrar_medicamento()
        elif opcion == "2":
            actualizar_stock()
        elif opcion == "3":
            mostrar_inventario()
        elif opcion == "4":
            verificar_alertas_inventario()
        elif opcion == "0":
            break
        else:
            print(MSG_OPCION_INVALIDA)


def seleccionar_paciente(id_propietario):
    mascotas = [p for p in pacientes.values() if p.id_propietario == id_propietario]
    if not mascotas:
        print("Este propietario no tiene pacientes registrados. Registremos uno.")
        registrar_paciente()
        mascotas = [p for p in pacientes.values() if p.id_propietario == id_propietario]
    if len(mascotas) == 1:
        return mascotas[0]
    print("¿Para cuál paciente es la cita?")
    for idx, m in enumerate(mascotas, 1):
        print(f"{idx}. {m.nombre}")
    while True:
        try:
            seleccion = int(input("Seleccione el número correspondiente: "))
            if 1 <= seleccion <= len(mascotas):
                return mascotas[seleccion - 1]
            else:
                print("⚠️ Selección fuera de rango. Intente de nuevo.")
        except ValueError:
            print("⚠️ Entrada no válida. Ingrese un número.")

def seleccionar_veterinario():
    veterinarios = cargar_veterinarios()
    if not veterinarios:
        print("❌ No hay veterinarios disponibles.")
        return None
    print("Veterinarios disponibles:")
    for idx, vet in enumerate(veterinarios, 1):
        print(f"{idx}. {vet['nombre']} (ID: {vet['id']})")
    while True:
        try:
            seleccion_vet = int(input("Seleccione el número correspondiente al veterinario: "))
            if 1 <= seleccion_vet <= len(veterinarios):
                return veterinarios[seleccion_vet - 1]["id"]
            else:
                print("⚠️ Selección fuera de rango. Intente de nuevo.")
        except ValueError:
            print("⚠️ Entrada no válida. Ingrese un número.")

def agendar_cita_mejorada():
    print("\n--- Agendar Cita Médica ---")
    id_propietario = input("Ingrese el ID del propietario: ")
    if id_propietario not in propietarios:
        print("Propietario no encontrado. Por favor regístrelo primero.")
        registrar_propietario()
        registrar_paciente()
        return
    paciente_seleccionado = seleccionar_paciente(id_propietario)
    fecha = input("Fecha (YYYY-MM-DD): ")
    hora = input("Hora (HH:MM): ")
    motivo = input("Motivo: ")
    id_veterinario = seleccionar_veterinario()
    if id_veterinario is None:
        return
    registrar_cita(fecha, hora, motivo, paciente_seleccionado.id, id_veterinario)


def menu():
    while True:
        print("\n" + "="*60)
        print("🐾 SISTEMA DE GESTIÓN VETERINARIA - PATITAS FELICES 🐾")
        print("="*60)
        print("📋 GESTIÓN BÁSICA")
        print("1.  Registrar propietario")
        print("2.  Registrar paciente")
        print("3.  Ver propietarios")
        print("4.  Ver pacientes")
        print("5.  Ver mascotas de un propietario")
        print("\n📅 GESTIÓN DE CITAS")
        print("6.  Menú de citas")
        print("\n📋 HISTORIA CLÍNICA")
        print("7.  Menú de historia clínica")
        print("\n💊 INVENTARIO")
        print("8.  Menú de inventario")
        print("\n✏️ EDICIÓN")
        print("9.  Editar datos")
        print("\n📊 REPORTES")
        print("10. Generar informe mensual")
        print("\n⚠️ ALERTAS")
        print("11. Verificar alertas de inventario")
        print("\n0.  Salir")
        print("="*60)
        
        # Mostrar alertas automáticamente
        verificar_alertas_inventario()
        opcion = input(PROMPT_SELECCIONE_OPCION)

        if opcion == "1":
            registrar_propietario()
        elif opcion == "2":
            registrar_paciente()
        elif opcion == "3":
            mostrar_propietarios()
        elif opcion == "4":
            mostrar_pacientes()
        elif opcion == "5":
            ver_mascotas_por_propietario()
        elif opcion == "6":
            submenu_citas()
        elif opcion == "7":
            submenu_historia_clinica()
        elif opcion == "8":
            submenu_inventario()
        elif opcion == "9":
            menu_editar_datos()
        elif opcion == "10":
            generar_informe_mensual()
        elif opcion == "11":
            verificar_alertas_inventario()
        elif opcion == "0":
            print("Hasta luego 🐾")
            print("¡Gracias por usar el Sistema de Gestión Veterinaria Patitas Felices!")
            break
        else:
            print(MSG_OPCION_INVALIDA)


if __name__ == "__main__":
    print("🐾 Bienvenido al Sistema de Gestión Veterinaria Patitas Felices 🐾")
    menu()
