import pytest

import bufalo.modulos.gestorInventario as gi


@pytest.fixture(autouse=True)
def limpiar_archivo():
    """Limpia el archivo antes y después de cada test."""
    if gi.INVENTARIO_FILE.exists():
        gi.INVENTARIO_FILE.unlink()
    yield
    if gi.INVENTARIO_FILE.exists():
        gi.INVENTARIO_FILE.unlink()


def test_agregar_producto():
    assert gi.agregar_producto("Coca", 5, 12.5) is True
    assert gi.agregar_producto("Coca", 10, 18) is False


def test_actualizar_producto():
    gi.agregar_producto("Pan", 20, 5)
    assert gi.actualizar_producto("Pan", cantidad=50) is True
    assert gi.actualizar_producto("Pan", precio=8) is True
    assert gi.actualizar_producto("X") is False


def test_eliminar_producto():
    gi.agregar_producto("Leche", 10, 20)
    assert gi.eliminar_producto("Leche") is True
    assert gi.eliminar_producto("Inexistente") is False


def test_consultar_y_listar():
    gi.agregar_producto("Arroz", 15, 22)
    item = gi.consultar_producto("Arroz")
    assert item["cantidad"] == 15
    assert "Arroz" in gi.listar_inventario()


def test_cargar_archivo_inexistente():
    if gi.INVENTARIO_FILE.exists():
        gi.INVENTARIO_FILE.unlink()
    assert gi._cargar_inventario() == {}


def test_cargar_json_invalido():
    gi.INVENTARIO_FILE.write_text("{esto no es json", encoding="utf-8")
    assert gi._cargar_inventario() == {}


def test_guardar_y_cargar():
    data = {"Test": {"cantidad": 1, "precio": 9.9}}
    gi._guardar_inventario(data)
    assert gi._cargar_inventario() == data


def test_guardar_inventario_oserror(monkeypatch):
    """Fuerza un OSError en _guardar_inventario para cubrir el bloque except."""

    def fake_open(*args, **kwargs):
        raise OSError("error simulado")

    # Reemplaza open() solo dentro de este test
    monkeypatch.setattr("builtins.open", fake_open)

    # No debe crashear aunque guardar falle
    gi._guardar_inventario({"x": 1})
