# 🎯 GUÍA DE USO DE LOS ARCHIVOS

## � main.py ⭐
**Propósito**: Sistema principal con opciones de inicio inteligentes
**Nuevas características**:
- 🔄 **Menú de inicio**: Elige entre cargar backup, datos de prueba o iniciar vacío
- 💾 **Gestión de backups**: Lista y carga backups automáticamente
- 🛠️ **Crear backups**: Opción en menú principal para backup manual
- 🔧 **Uso real o demostración**: Adaptable a cualquier necesidad

**Cuándo usar**:
- ✅ **RECOMENDADO PRINCIPAL**: Para cualquier uso del sistema
- ✅ Para usar backups existentes
- ✅ Para empezar desde cero o con datos de prueba
- ✅ Para uso real en clínica
- ✅ Para crear backups manuales

**Comando**: `python main.py`

---

## 📋 datos_prueba.py
**Propósito**: Generar y cargar datos de prueba únicamente
**Cuándo usar**:
- ✅ Solo para cargar datos sin abrir el menú
- ✅ Para resetear/recargar datos limpios
- ✅ Para importar en otros scripts
- ✅ Para ver el resumen de datos sin usar el sistema

**Comando**: `python datos_prueba.py`

## � analizador_backup.py
**Propósito**: Analizar y comparar archivos de backup
**Cuándo usar**:
- ✅ Para verificar integridad de backups
- ✅ Para comparar diferentes backups
- ✅ Para estadísticas detalladas de datos guardados

**Comando**: `python analizador_backup.py`

## 🧪 test_sistema.py
**Propósito**: Pruebas automatizadas del sistema
**Cuándo usar**:
- ✅ Para verificar funcionamiento correcto
- ✅ Antes de realizar cambios importantes
- ✅ Para validar integridad de datos

**Comando**: `python test_sistema.py`

---

## 🎯 FLUJO RECOMENDADO ACTUALIZADO:

### 📚 **Para explorar/demostrar el sistema:**
```bash
python main.py
# Seleccionar opción 2: "Cargar datos de prueba"
```

### 💼 **Para uso real en clínica:**
```bash
python main.py
# Seleccionar opción 1: "Cargar desde backup" (si existe)
# O opción 3: "Iniciar con sistema vacío" (primera vez)
```

### 🔄 **Para resetear datos:**
```bash
python datos_prueba.py  # Solo cargar datos
# O usar main.py > opción 2 (RECOMENDADO)
```

### 💾 **Para trabajar con backups:**
```bash
python main.py
# Opción 1 para cargar backup existente
# En menú principal > opción 11 para crear nuevo backup
```

### 🔍 **Para análisis de datos:**
```bash
python analizador_backup.py  # Analizar backups
python test_sistema.py       # Verificar sistema
```

---

## 📁 **ESTRUCTURA SIMPLIFICADA:**

```
Patitas-felices/
├── main.py                    ⭐ ARCHIVO PRINCIPAL - USAR ESTE
├── datos_prueba.py           📊 Para datos de demostración
├── analizador_backup.py      🔍 Para análisis de backups  
├── test_sistema.py           🧪 Para pruebas del sistema

```

