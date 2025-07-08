# Base de datos en memoria mejorada para el Sistema Veterinario Patitas Felices
from datetime import datetime
import json
import os

# Diccionarios que actúan como "base de datos en memoria"
propietarios = {}
pacientes = {}
citas_registradas = []
medicamentos = {}
historias_clinicas = []

# Configuración de persistencia
DATA_DIR = "data"
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

def crear_directorios():
    """Crear directorios necesarios si no existen"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def obtener_estadisticas():
    """Obtener estadísticas generales del sistema"""
    stats = {
        "propietarios": len(propietarios),
        "pacientes": len(pacientes),
        "citas_total": len(citas_registradas),
        "citas_agendadas": len([c for c in citas_registradas if c.estado == "agendada"]),
        "citas_realizadas": len([c for c in citas_registradas if c.estado == "realizada"]),
        "citas_canceladas": len([c for c in citas_registradas if c.estado == "cancelada"]),
        "medicamentos": len(medicamentos),
        "stock_bajo": len([m for m in medicamentos.values() if int(m.stock) <= 10]),
        "historias_clinicas": len(historias_clinicas),
        "ultima_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return stats

def validar_integridad_datos():
    """Validar la integridad de los datos en memoria"""
    errores = []
    
    # Verificar que todos los pacientes tengan propietarios válidos
    for paciente in pacientes.values():
        if paciente.id_propietario not in propietarios:
            errores.append(f"Paciente {paciente.nombre} (ID: {paciente.id}) tiene propietario inválido: {paciente.id_propietario}")
    
    # Verificar que las citas tengan pacientes válidos
    for cita in citas_registradas:
        if cita.id_paciente not in pacientes:
            errores.append(f"Cita {cita.id} tiene paciente inválido: {cita.id_paciente}")
    
    # Verificar que las historias clínicas tengan pacientes válidos
    for historia in historias_clinicas:
        if historia.id_paciente not in pacientes:
            errores.append(f"Historia clínica {historia.id} tiene paciente inválido: {historia.id_paciente}")
    
    return errores

def limpiar_datos():
    """Limpiar todos los datos en memoria"""
    propietarios.clear()
    pacientes.clear()
    citas_registradas.clear()
    medicamentos.clear()
    historias_clinicas.clear()
    print("🗑️ Datos limpiados correctamente")

def exportar_datos_json(archivo="backup_datos.json"):
    """Exportar todos los datos a un archivo JSON"""
    try:
        crear_directorios()
        datos = {
            "propietarios": {id: {
                "id": prop.id,
                "nombre": prop.nombre,
                "telefono": prop.telefono,
                "correo": prop.correo,
                "direccion": prop.direccion,
                "mascotas": prop.mascotas
            } for id, prop in propietarios.items()},
            
            "pacientes": {id: {
                "id": pac.id,
                "nombre": pac.nombre,
                "edad": pac.edad,
                "especie": pac.especie,
                "raza": pac.raza,
                "peso": pac.peso,
                "sexo": pac.sexo,
                "id_propietario": pac.id_propietario
            } for id, pac in pacientes.items()},
            
            "citas": [{
                "id": cita.id,
                "fecha": cita.fecha,
                "hora": cita.hora,
                "motivo": cita.motivo,
                "id_paciente": cita.id_paciente,
                "id_veterinario": cita.id_veterinario,
                "estado": cita.estado
            } for cita in citas_registradas],
            
            "medicamentos": {id: {
                "id": med.id,
                "nombre": med.nombre,
                "descripcion": med.descripcion,
                "stock": med.stock,
                "fecha_vencimiento": med.fecha_vencimiento,
                "precio": med.precio
            } for id, med in medicamentos.items()},
            
            "historias_clinicas": [{
                "id": hist.id,
                "id_paciente": hist.id_paciente,
                "diagnostico": hist.diagnostico,
                "tratamiento": hist.tratamiento,
                "vacunas": hist.vacunas,
                "observaciones": hist.observaciones,
                "fecha": hist.fecha_actualizacion
            } for hist in historias_clinicas],
            
            "metadata": {
                "fecha_exportacion": datetime.now().isoformat(),
                "version": "1.0",
                "estadisticas": obtener_estadisticas()
            }
        }
        
        archivo_path = os.path.join(BACKUP_DIR, archivo)
        with open(archivo_path, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Datos exportados exitosamente a: {archivo_path}")
        return archivo_path
    
    except Exception as e:
        print(f"❌ Error al exportar datos: {e}")
        return None

def mostrar_resumen_sistema():
    """Mostrar un resumen completo del estado del sistema"""
    stats = obtener_estadisticas()
    errores = validar_integridad_datos()
    
    print("\n" + "="*50)
    print("📊 RESUMEN DEL SISTEMA")
    print("="*50)
    print(f"👥 Propietarios: {stats['propietarios']}")
    print(f"🐾 Pacientes: {stats['pacientes']}")
    print("📅 Citas:")
    print(f"   • Total: {stats['citas_total']}")
    print(f"   • Agendadas: {stats['citas_agendadas']}")
    print(f"   • Realizadas: {stats['citas_realizadas']}")
    print(f"   • Canceladas: {stats['citas_canceladas']}")
    print("💊 Inventario:")
    print(f"   • Medicamentos: {stats['medicamentos']}")
    print(f"   • Stock bajo: {stats['stock_bajo']}")
    print(f"📋 Historias clínicas: {stats['historias_clinicas']}")
    print(f"🕒 Última actualización: {stats['ultima_actualizacion']}")
    
    if errores:
        print("\n⚠️ ERRORES DE INTEGRIDAD:")
        for error in errores:
            print(f"   • {error}")
    else:
        print("\n✅ Integridad de datos: OK")
    
    print("="*50)
