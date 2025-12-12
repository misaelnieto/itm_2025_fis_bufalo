import json
from pathlib import Path

# Definimos la ruta del archivo de preferencias que se creará en la raíz del proyecto
PREFS_FILE = Path("configuracion.json") 


# ==========================
# FUNCIONES INTERNAS DE GESTIÓN
# ==========================


def _cargar_preferencias():
    """
    Carga las preferencias de configuración desde el archivo JSON.
    Si no existe o está dañado, regresa la configuración por defecto.
    """
    # 1. Configuración por defecto (DEFAULT)
    DEFAULTS = {
        "unidad_preferida": "C",  # C para Celsius, F para Fahrenheit
        "decimales": 2
    }

    if not PREFS_FILE.exists():
        # Si el archivo no existe, simplemente retorna los valores por defecto
        return DEFAULTS

    try:
        # Intenta abrir y leer el archivo
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            # Intenta cargar el contenido JSON
            preferencias = json.load(f)
            # Combina con los valores por defecto (asegura que siempre haya valores válidos)
            return DEFAULTS | preferencias 

    except json.JSONDecodeError:
        # Si el archivo está vacío o tiene formato incorrecto
        print("ADVERTENCIA: Archivo de configuración corrupto o vacío. Usando preferencias por defecto.")
        return DEFAULTS
    
    except Exception as e:
        # Manejo de otros errores de lectura
        print(f"ERROR: No se pudo leer el archivo de configuración: {e}")
        return DEFAULTS


def _guardar_preferencias(prefs):
    """
    Guarda el diccionario de preferencias en el archivo JSON.
    """
    try:
        with open(PREFS_FILE, "w", encoding="utf-8") as f:
            # Guarda el diccionario con formato (indent=4)
            json.dump(prefs, f, indent=4)
    except Exception as e:
        print(f"ERROR: No se pudo guardar la configuración: {e}")


# ==========================
# FUNCIONES PÚBLICAS
# ==========================

def obtener_preferencias():
    """
    Función pública para obtener todas las preferencias actuales.
    Retorna un diccionario con la configuración.
    """
    return _cargar_preferencias()


def establecer_preferencia(clave, valor):
    """
    Función pública para establecer (cambiar) una preferencia específica
    y guardar los cambios en el archivo.
    """
    # 1. Cargar las preferencias actuales
    prefs = _cargar_preferencias()
    
    # 2. Modificar la clave deseada
    if clave in prefs:
        prefs[clave] = valor
        
        # 3. Guardar el diccionario modificado
        _guardar_preferencias(prefs)
        return True
    else:
        print(f"ERROR: La clave '{clave}' no existe en las preferencias por defecto.")
        return False