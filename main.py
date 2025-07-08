from servicios.registro_propietario import registrar_propietario
from servicios.registro_paciente import registrar_paciente, ver_mascotas_por_propietario
from servicios.registro_cita import registrar_cita
from servicios.gestion_citas import ver_citas, cancelar_cita, buscar_citas_por_fecha
from servicios.historia_clinica import crear_historia_clinica, consultar_historial_paciente, registrar_atencion_medica
from servicios.inventario_medicamentos import registrar_medicamento, actualizar_stock, mostrar_inventario, verificar_alertas_inventario
from servicios.editar_datos import menu_editar_datos
from servicios.informes import generar_informe_mensual
from data.db import propietarios, pacientes, citas_registradas
import json
import os
from datetime import datetime

JSON_EXTENSION = '.json'
MENU_VOLVER_PRINCIPAL = "0. Volver al menú principal"
PROMPT_SELECCIONE_OPCION = "Seleccione una opción: "
MSG_OPCION_INVALIDA = "❌ Opción inválida. Intente de nuevo."
MSG_ENTRADA_NO_VALIDA = "⚠️ Entrada no válida. Ingrese un número."

def listar_backups_disponibles():
    """Lista todos los backups disponibles"""
    backup_dir = "data/backups"
    if not os.path.exists(backup_dir):
        return []
    
    backups = []
    for archivo in os.listdir(backup_dir):
        if archivo.endswith(JSON_EXTENSION):
            ruta_completa = os.path.join(backup_dir, archivo)
            fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
            backups.append({
                'archivo': archivo,
                'ruta': ruta_completa,
                'fecha': fecha_mod
            })
    
    # Ordenar por fecha (más reciente primero)
    backups.sort(key=lambda x: x['fecha'], reverse=True)
    return backups

def cargar_backup_interactivo():
    """Permite al usuario seleccionar y cargar un backup"""
    backups = listar_backups_disponibles()
    
    if not backups:
        print("❌ No hay backups disponibles.")
        respuesta = input("¿Desea cargar datos de prueba en su lugar? (s/n): ")
        if respuesta.lower() == 's':
            from datos_prueba import cargar_datos_prueba
            cargar_datos_prueba()
            return True
        return False
    
    print("\n📁 BACKUPS DISPONIBLES:")
    print("="*50)
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup['archivo']}")
        print(f"   📅 Fecha: {backup['fecha'].strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    print("0. No cargar backup (sistema vacío)")
    print("99. Cargar datos de prueba")
    
    while True:
        try:
            seleccion = int(input("Seleccione el backup a cargar: "))
            
            if seleccion == 0:
                print("✅ Iniciando con sistema vacío.")
                return False
            elif seleccion == 99:
                from datos_prueba import cargar_datos_prueba
                cargar_datos_prueba()
                return True
            elif 1 <= seleccion <= len(backups):
                backup_seleccionado = backups[seleccion - 1]
                return cargar_backup_desde_archivo(backup_seleccionado['ruta'])
            else:
                print("⚠️ Selección fuera de rango.")
        except ValueError:
            print(MSG_ENTRADA_NO_VALIDA)

def cargar_backup_desde_archivo(ruta_backup):
    """Carga datos desde un archivo de backup específico"""
    try:
        print(f"🔄 Cargando backup: {os.path.basename(ruta_backup)}")
        
        with open(ruta_backup, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        # Importar las clases necesarias
        from modelos.propietario import Propietario
        from modelos.paciente import Paciente
        from modelos.cita import Cita
        from modelos.medicamento import Medicamento
        from modelos.historia_clinica import HistoriaClinica
        from data.db import medicamentos, historias_clinicas
        
        # Limpiar datos actuales
        propietarios.clear()
        pacientes.clear()
        citas_registradas.clear()
        medicamentos.clear()
        historias_clinicas.clear()
        
        # Determinar estructura del backup (nueva vs antigua)
        if 'datos' in backup_data:
            # Estructura nueva con 'datos' wrapper
            datos = backup_data['datos']
            metadatos = backup_data.get('metadatos', {})
        else:
            # Estructura antigua - datos directamente en la raíz
            datos = backup_data
            metadatos = backup_data.get('metadata', {})
        
        # Cargar propietarios
        for prop_id, prop_data in datos['propietarios'].items():
            prop = Propietario(
                prop_data['id'],
                prop_data['nombre'],
                prop_data['telefono'],
                prop_data['correo'],
                prop_data['direccion']
            )
            prop.mascotas = prop_data['mascotas']
            propietarios[prop_id] = prop
        
        # Cargar pacientes
        for pac_id, pac_data in datos['pacientes'].items():
            pac = Paciente(
                pac_data['id'],
                pac_data['nombre'],
                pac_data['edad'],
                pac_data['especie'],
                pac_data['raza'],
                pac_data['peso'],
                pac_data['sexo'],
                pac_data['id_propietario']
            )
            pacientes[pac_id] = pac
        
        # Cargar citas (puede estar como 'citas' o 'citas_registradas')
        citas_data = datos.get('citas', datos.get('citas_registradas', []))
        for cita_data in citas_data:
            cita = Cita(
                cita_data['id'],
                cita_data['fecha'],
                cita_data['hora'],
                cita_data['motivo'],
                cita_data['id_paciente'],
                cita_data['id_veterinario'],
                cita_data['estado']
            )
            citas_registradas.append(cita)
        
        # Cargar medicamentos
        for med_id, med_data in datos['medicamentos'].items():
            med = Medicamento(
                med_data['id'],
                med_data['nombre'],
                med_data['descripcion'],
                med_data['stock'],  # Mantener como número
                med_data['fecha_vencimiento'],
                med_data['precio']
            )
            medicamentos[med_id] = med
        
        # Cargar historias clínicas
        for hist_data in datos['historias_clinicas']:
            hist = HistoriaClinica(
                hist_data['id'],
                hist_data['id_paciente'],
                hist_data['diagnostico'],
                hist_data['tratamiento'],
                hist_data['vacunas'],
                hist_data['observaciones']
            )
            # Agregar fecha si existe
            if 'fecha' in hist_data:
                hist.fecha = hist_data['fecha']
            historias_clinicas.append(hist)
        
        print("✅ Backup cargado exitosamente!")
        print("📊 Datos restaurados:")
        print(f"   • {len(propietarios)} propietarios")
        print(f"   • {len(pacientes)} pacientes") 
        print(f"   • {len(citas_registradas)} citas")
        print(f"   • {len(medicamentos)} medicamentos")
        print(f"   • {len(historias_clinicas)} historias clínicas")
        
        # Mostrar fecha del backup si está disponible
        fecha_backup = metadatos.get('fecha_exportacion') or metadatos.get('fecha_creacion', 'No disponible')
        print(f"📅 Backup del: {fecha_backup}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al cargar backup: {e}")
        print(f"🔍 Detalles del error: {type(e).__name__}")
        return False

def mostrar_menu_inicial():
    """Muestra menú inicial para elegir modo de inicio"""
    print("🐾 Bienvenido al Sistema de Gestión Veterinaria Patitas Felices 🐾")
    print("\n🚀 ¿CÓMO DESEA INICIAR EL SISTEMA?")
    print("="*50)
    print("1. 📁 Cargar backup de días anteriores")
    print("2. 📊 Cargar datos de prueba (demostración)")
    print("3. 🆕 Iniciar con sistema vacío")
    print("="*50)
    
    while True:
        try:
            opcion = int(input("Seleccione una opción (1-3): "))
            
            if opcion == 1:
                return cargar_backup_interactivo()
            elif opcion == 2:
                from datos_prueba import cargar_datos_prueba
                cargar_datos_prueba()
                return True
            elif opcion == 3:
                print("✅ Iniciando con sistema vacío.")
                return False
            else:
                print("⚠️ Opción inválida. Seleccione 1, 2 o 3.")
        except ValueError:
            print(MSG_ENTRADA_NO_VALIDA)

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
            print(MSG_ENTRADA_NO_VALIDA)

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


def handle_menu_option(opcion):
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
        crear_backup_manual()
    elif opcion == "12":
        verificar_alertas_inventario()
    elif opcion == "0":
        print("Hasta luego 🐾")
        print("¡Gracias por usar el Sistema de Gestión Veterinaria Patitas Felices!")
        return False
    else:
        print(MSG_OPCION_INVALIDA)
    return True

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
        print("\n💾 BACKUP")
        print("11. Crear backup de datos")
        print("\n⚠️ ALERTAS")
        print("12. Verificar alertas de inventario")
        print("\n0.  Salir")
        print("="*60)
        
        # Mostrar alertas automáticamente
        verificar_alertas_inventario()
        opcion = input(PROMPT_SELECCIONE_OPCION)

        if not handle_menu_option(opcion):
            break


def crear_backup_manual():
    """Permite crear un backup manual con nombre personalizado"""
    from data.db import exportar_datos_json
    
    print("\n💾 --- Crear Backup Manual ---")
    
    # Sugerir nombre por defecto
    fecha_actual = datetime.now().strftime("%Y%m%d_%H%M")
    nombre_sugerido = f"backup_manual_{fecha_actual}.json"
    
    print(f"📝 Nombre sugerido: {nombre_sugerido}")
    nombre = input("Ingrese nombre del backup (Enter para usar sugerido): ").strip()
    
    if not nombre:
        nombre = nombre_sugerido
    if not nombre.endswith(JSON_EXTENSION):
        nombre += JSON_EXTENSION
    
    try:
        exportar_datos_json(nombre)
        print(f"✅ Backup creado exitosamente: {nombre}")
        print("💡 Puede cargar este backup la próxima vez usando la opción 1 del menú inicial.")
    except Exception as e:
        print(f"❌ Error al crear backup: {e}")

if __name__ == "__main__":
    # Mostrar menú inicial para elegir modo de inicio
    datos_cargados = mostrar_menu_inicial()
    
    if datos_cargados:
        print("\n🎯 ¡Sistema listo para continuar trabajando!")
        print("💡 Sus datos están cargados y listos para usar.")
    else:
        print("\n🆕 Sistema iniciado vacío.")
        print("💡 Puede comenzar registrando propietarios y pacientes.")
    
    # Ejecutar el menú principal
    menu()
