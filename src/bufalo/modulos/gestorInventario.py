import json
from pathlib import Path

INVENTARIO_FILE = Path("inventario.json")


# ==========================
# FUNCIONES INTERNAS
# ==========================


def _cargar_inventario():
    """
    Carga el inventario desde el archivo JSON.
    Si no existe o está dañado, regresa {}.
    """
    if not INVENTARIO_FILE.exists():
        return {}

    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _guardar_inventario(data):
    """Guarda el inventario completo en el archivo JSON."""
    try:
        with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError:
        pass  # No debería ocurrir, pero evita crasheos en tests


def _buscar_producto(nombre):
    """Función auxiliar usada por los tests."""
    return _cargar_inventario().get(nombre)


# ==========================
# FUNCIONES PÚBLICAS
# ==========================


def agregar_producto(nombre, cantidad, precio):
    """Agrega un producto nuevo al inventario."""
    inventario = _cargar_inventario()

    if nombre in inventario:
        return False

    inventario[nombre] = {"cantidad": cantidad, "precio": precio}
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
    """Consulta un solo producto."""
    return _buscar_producto(nombre)


def listar_inventario():
    """Regresa el inventario completo."""
    return _cargar_inventario()


__all__ = [
    "_buscar_producto",
    "_cargar_inventario",
    "_guardar_inventario",
    "agregar_producto",
    "actualizar_producto",
    "eliminar_producto",
    "consultar_producto",
    "listar_inventario",
]
