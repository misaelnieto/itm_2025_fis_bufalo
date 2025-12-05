import json
import pytest
from pathlib import Path


def test_agregar(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    fake.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import agregar_producto, consultar_producto

    r = agregar_producto("Manzanas", 10, 5.0)
    assert r is True

    data = consultar_producto("Manzanas")
    assert data["cantidad"] == 10
    assert data["precio"] == 5.0


def test_agregar_existente(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    fake.write_text(json.dumps({"Pan": {"cantidad": 4, "precio": 12.0}}), encoding="utf-8")

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import agregar_producto

    r = agregar_producto("Pan", 8, 15.0)
    assert r is False


def test_actualizar(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    fake.write_text(
        json.dumps({"Coca": {"cantidad": 5, "precio": 20}}),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import actualizar_producto, consultar_producto

    r = actualizar_producto("Coca", cantidad=9, precio=22)
    assert r is True

    data = consultar_producto("Coca")
    assert data["cantidad"] == 9
    assert data["precio"] == 22


def test_eliminar(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    fake.write_text(
        json.dumps({"Huevos": {"cantidad": 30, "precio": 3.5}}),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import eliminar_producto, consultar_producto

    r = eliminar_producto("Huevos")
    assert r is True

    assert consultar_producto("Huevos") is None


def test_listar(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    data = {
        "Uno": {"cantidad": 1, "precio": 10},
        "Dos": {"cantidad": 2, "precio": 20},
    }
    fake.write_text(json.dumps(data), encoding="utf-8")

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import listar_inventario

    r = listar_inventario()
    assert r == data


def test_buscar_aux_inexistente(monkeypatch, tmp_path):
    fake = tmp_path / "inv.json"
    fake.write_text("{}", encoding="utf-8")

    monkeypatch.setattr(
        "bufalo.modulos.gestorInventario.INVENTARIO_FILE",
        fake
    )

    from bufalo.modulos.gestorInventario import _buscar_producto

    r = _buscar_producto("NO_EXISTE")
    assert r is None
