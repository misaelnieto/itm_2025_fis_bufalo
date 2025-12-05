import json
from pathlib import Path

INVENTARIO_FILE = Path("inventario.json")


def _cargar_inventario():
    """Carga el inventario desde el archivo JSON."""
    if not INVENTARIO_FILE.exists():
        return {}
    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def _guardar_inventario(data):
    """Guarda el inventario completo en el archivo JSON."""
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _buscar_producto(nombre):
    """Función auxiliar usada por los tests."""
    inventario = _cargar_inventario()
    return inventario.get(nombre)


def agregar_producto(nombre, cantidad, precio):
    """Agrega un producto nuevo al inventario."""
    inventario = _cargar_inventario()

    if nombre in inventario:
        return False

    inventario[nombre] = {
        "cantidad": cantidad,
        "precio": precio
    }

    _guardar_inventario(inventario)
    return True


def actualizar_producto(nombre, cantidad=None, precio=None):
    """Actualiza datos de un producto existente."""
    inventario = _cargar_inventario()

    if nombre not in inventario:
        return False

    if cantidad is not None:
        inventario[nombre]["cantidad"] = cantidad
    if precio is not None:
        inventario[nombre]["precio"] = precio

    _guardar_inventario(inventario)
    return True


def eliminar_producto(nombre):
    """Elimina un producto del inventario."""
    inventario = _cargar_inventario()

    if nombre not in inventario:
        return False

    del inventario[nombre]
    _guardar_inventario(inventario)
    return True


def consultar_producto(nombre):
    """Consulta la información de un producto."""
    return _buscar_producto(nombre)


def listar_inventario():
    """Regresa el inventario completo."""
    return _cargar_inventario()


# --------------------------------------------------
# EXPORTS PARA QUE PYTEST PUEDA IMPORTAR FUNCIONES PRIVADAS
# --------------------------------------------------
__all__ = [
    "_buscar_producto",
    "agregar_producto",
    "actualizar_producto",
    "eliminar_producto",
    "consultar_producto",
    "listar_inventario",
]
