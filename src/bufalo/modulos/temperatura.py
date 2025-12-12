# --- INICIO DEL ARCHIVO temperatura.py ---

# Importamos la función que nos permite leer la configuración global
from bufalo.config.preferencias import obtener_preferencias

def c_a_f(celsius):
    """Convierte Celsius a Fahrenheit y aplica el redondeo de las preferencias."""
    
    # 1. Obtener la configuración
    config = obtener_preferencias()
    decimales = config["decimales"] 
    
    # 2. Realizar la conversión
    resultado = (celsius * 9/5) + 32
    
    # 3. Aplicar redondeo
    return round(resultado, decimales)


def f_a_c(fahrenheit):
    """Convierte Fahrenheit a Celsius y aplica el redondeo de las preferencias."""
    
    # 1. Obtener la configuración
    config = obtener_preferencias()
    decimales = config["decimales"] 
    
    # 2. Realizar la conversión
    resultado = (fahrenheit - 32) * 5/9
    
    # 3. Aplicar redondeo
    return round(resultado, decimales)


def convertir(valor_actual):
    """
    Convierte un valor de temperatura al formato de unidad preferida del usuario.
    Asume que el valor actual está en la unidad OPUESTA a la preferida.
    """
    config = obtener_preferencias()
    unidad_preferida = config["unidad_preferida"]
    
    # Si la preferencia es Celsius, asumimos que el valor actual es Fahrenheit
    if unidad_preferida == "C":
        # Llama a la función que convierte a Celsius
        return f_a_c(valor_actual) 
    
    # Si la preferencia es Fahrenheit, asumimos que el valor actual es Celsius
    elif unidad_preferida == "F":
        # Llama a la función que convierte a Fahrenheit
        return c_a_f(valor_actual) 
    
    else:
        # Esto maneja un error si la preferencia no es 'C' ni 'F'
        print("ADVERTENCIA: Unidad preferida no válida. Usando Celsius por defecto.")
        return f_a_c(valor_actual)

# --- FIN DEL ARCHIVO temperatura.py ---