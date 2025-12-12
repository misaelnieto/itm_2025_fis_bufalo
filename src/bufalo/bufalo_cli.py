import argparse
import sys
import os

# 1. Configuración de Rutas: Esencial para que 'uv run' encuentre tu carpeta 'src'
# Añade la ruta del directorio actual (la raíz del proyecto) al path de Python.
sys.path.insert(0, os.path.dirname(__file__))

# 2. Importación de Módulos: Llamamos a las funciones que ya escribiste y probaste.
from src.bufalo.modulos.temperatura import convertir as convertir_temp
from src.bufalo.modulos.moneda import convertir_a_moneda
from src.bufalo.config.preferencias import establecer_preferencia

# --- LÓGICA DE MANEJO DE MÓDULOS ---

def manejar_temperatura(args):
    """Maneja la lógica para el módulo 'bufalo temperatura'."""
    
    # Validación de entrada
    try:
        valor = float(args.valor)
    except ValueError:
        print("Error: El valor de temperatura debe ser un número válido.")
        return

    # Establecer la preferencia de la unidad para que tu función la use
    unidad_destino = args.unidad_destino.upper()
    establecer_preferencia("unidad_preferida", unidad_destino)
    establecer_preferencia("decimales", 2) # Aseguramos 2 decimales para la salida CLI
    
    if args.action == 'convertir':
        # Llamada a tu función probada (temperatura.py)
        # La función 'convertir' sabe asumir la unidad opuesta y convertirla a la preferida.
        resultado = convertir_temp(valor)
        print(f"Resultado: {resultado} {unidad_destino}")

def manejar_moneda(args):
    """Maneja la lógica para el módulo 'bufalo moneda'."""
    
    try:
        monto = float(args.monto)
    except ValueError:
        print("Error: El monto debe ser un número válido.")
        return

    # Aseguramos 2 decimales para la salida financiera
    establecer_preferencia("decimales", 2) 

    if args.action == 'usd-eur':
        # Llamada a tu función probada (moneda.py)
        resultado = convertir_a_moneda(monto, "EUR")
        print(f"Resultado: {resultado} EUR")

# --- CONFIGURACIÓN DEL PARSER PRINCIPAL (argparse) ---

def main():
    """Función principal que despacha los comandos CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema CLI para cálculos de Búfalo (Temperatura y Moneda).",
        usage="""uv run bufalo <módulo> <acción> ..."""
    )
    
    # Sub-parsers: Define los módulos principales (temperatura, moneda)
    subparsers = parser.add_subparsers(title='Módulos', dest='modulo')

    # === 1. MÓDULO TEMPERATURA ===
    parser_temp = subparsers.add_parser('temperatura', help='Herramientas de conversión de temperatura.')
    parser_temp.set_defaults(func=manejar_temperatura)
    
    temp_subparsers = parser_temp.add_subparsers(title='Acciones de Temp', dest='action', required=True)
    
    # Comando: bufalo temperatura convertir <valor> <unidad_destino>
    parser_convert = temp_subparsers.add_parser('convertir', help='Convierte al formato de unidad deseada (C o F).')
    parser_convert.add_argument('valor', type=str, help='El valor numérico a convertir (ej: 25).')
    parser_convert.add_argument('unidad_destino', type=str, choices=['C', 'F', 'c', 'f'], help='Unidad final deseada (C o F).')
    

    # === 2. MÓDULO MONEDA ===
    parser_moneda = subparsers.add_parser('moneda', help='Herramientas de conversión de divisas.')
    parser_moneda.set_defaults(func=manejar_moneda)
    
    moneda_subparsers = parser_moneda.add_subparsers(title='Acciones de Moneda', dest='action', required=True)
    
    # Comando: bufalo moneda usd-eur <monto>
    parser_usd_eur = moneda_subparsers.add_parser('usd-eur', help='Convierte USD a EUR.')
    parser_usd_eur.add_argument('monto', type=str, help='El monto en USD a convertir (ej: 100.50).')

    # Ejecución
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()