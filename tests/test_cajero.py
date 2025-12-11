"""
Pruebas unitarias para el módulo de cajero automático.

Este archivo contiene todas las pruebas para verificar que los comandos
del cajero automático funcionan correctamente. Las pruebas se ejecutan con pytest.

Para ejecutar estas pruebas:
    uv run pytest tests/test_cajero.py -v

Para ver el coverage:
    uv run pytest tests/test_cajero.py --cov=src.bufalo.modulos.cajero \
    --cov-report=term-missing
"""

import json
import os
import tempfile
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bufalo.modulos.cajero import (
    cajero,
    cargar_estado,
    guardar_estado,
)


@pytest.fixture
def temp_estado_file() -> str:
    """Fixture para crear un archivo temporal para el estado"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def runner() -> CliRunner:
    """Fixture para CliRunner"""
    return CliRunner()


# ==================== TESTS PARA cargar_estado() ====================


def test_cargar_estado_archivo_no_existe() -> None:
    """
    Prueba que cargar_estado devuelve valores por defecto cuando el archivo no existe.

    Cuando el archivo de estado no existe, debe retornar:
    - saldo: 1000.0
    - movimientos: []
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", "archivo_inexistente.json"):
        saldo_result, movimientos_result = cargar_estado()
        assert saldo_result == 1000.0
        assert movimientos_result == []


def test_cargar_estado_archivo_json_valido(temp_estado_file: str) -> None:
    """
    Prueba que cargar_estado carga correctamente un archivo JSON válido.

    El archivo contiene saldo y movimientos, y deben cargarse correctamente.
    """
    estado = {"saldo": 500.0, "movimientos": ["Retiro: -$500"]}
    with open(temp_estado_file, "w") as f:
        json.dump(estado, f)

    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        saldo_result, movimientos_result = cargar_estado()
        assert saldo_result == 500.0
        assert movimientos_result == ["Retiro: -$500"]


def test_cargar_estado_json_corrupto(temp_estado_file: str) -> None:
    """
    Prueba que cargar_estado maneja archivos con JSON corrupto.

    Cuando el archivo tiene JSON inválido, debe retornar valores por defecto
    sin lanzar una excepción.
    """
    with open(temp_estado_file, "w") as f:
        f.write("{ json invalido }")

    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        saldo_result, movimientos_result = cargar_estado()
        assert saldo_result == 1000.0
        assert movimientos_result == []


def test_cargar_estado_archivo_sin_saldo(temp_estado_file: str) -> None:
    """
    Prueba que cargar_estado maneja archivos sin la clave 'saldo'.

    Cuando falta la clave 'saldo', debe usar 1000.0 como valor por defecto.
    """
    estado = {"movimientos": ["Depósito: +$1000"]}
    with open(temp_estado_file, "w") as f:
        json.dump(estado, f)

    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        saldo_result, movimientos_result = cargar_estado()
        assert saldo_result == 1000.0
        assert movimientos_result == ["Depósito: +$1000"]


def test_cargar_estado_archivo_sin_movimientos(temp_estado_file: str) -> None:
    """
    Prueba que cargar_estado maneja archivos sin la clave 'movimientos'.

    Cuando falta la clave 'movimientos', debe usar una lista vacía como
    valor por defecto.
    """
    estado = {"saldo": 750.0}
    with open(temp_estado_file, "w") as f:
        json.dump(estado, f)

    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        saldo_result, movimientos_result = cargar_estado()
        assert saldo_result == 750.0
        assert movimientos_result == []


# ==================== TESTS PARA guardar_estado() ====================


def test_guardar_estado_crea_archivo(temp_estado_file: str) -> None:
    """
    Prueba que guardar_estado crea el archivo correctamente.

    Debe crear un archivo JSON con la estructura: {"saldo": X, "movimientos": [...]}
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        guardar_estado(2000.0, ["Depósito: +$1000"])

        with open(temp_estado_file, "r") as f:
            estado = json.load(f)

        assert estado["saldo"] == 2000.0
        assert estado["movimientos"] == ["Depósito: +$1000"]


def test_guardar_estado_sobrescribe_archivo(temp_estado_file: str) -> None:
    """
    Prueba que guardar_estado sobrescribe el contenido anterior.

    Cuando se llama guardar_estado dos veces, el contenido anterior debe
    ser reemplazado.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        guardar_estado(1000.0, ["Primero"])
        guardar_estado(2000.0, ["Primero", "Segundo"])

        with open(temp_estado_file, "r") as f:
            estado = json.load(f)

        assert estado["saldo"] == 2000.0
        assert len(estado["movimientos"]) == 2


# ==================== TESTS PARA COMANDO consultar ====================


def test_consultar_pin_correcto(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'consultar' con PIN correcto.

    Cuando se proporciona el PIN correcto (1234), el comando debe mostrar el saldo.
    """
    with patch("bufalo.modulos.cajero.saldo", 1500.0):
        with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
            result = runner.invoke(cajero, ["consultar", "--pin-input", "1234"])
            assert result.exit_code == 0
            assert "Saldo:" in result.output
            assert "$1500" in result.output


def test_consultar_pin_incorrecto(runner: CliRunner) -> None:
    """
    Prueba el comando 'consultar' con PIN incorrecto.

    Cuando se proporciona un PIN incorrecto, el comando debe mostrar un
    mensaje de error.
    """
    result = runner.invoke(cajero, ["consultar", "--pin-input", "9999"])
    assert result.exit_code == 0
    assert "PIN incorrecto" in result.output


# ==================== TESTS PARA COMANDO depositar ====================


def test_depositar_pin_correcto_monto_positivo(
    runner: CliRunner, temp_estado_file: str
) -> None:
    """
    Prueba el comando 'depositar' con PIN correcto y monto positivo.

    Cuando se proporciona el PIN correcto y un monto positivo, el comando debe:
    - Mostrar el monto depositado
    - Mostrar el nuevo saldo
    - Guardar el movimiento en el archivo
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["depositar", "500", "--pin-input", "1234"])
        assert result.exit_code == 0
        assert "Depositado:" in result.output
        assert "$500" in result.output
        assert "Nuevo saldo:" in result.output


def test_depositar_pin_incorrecto(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'depositar' con PIN incorrecto.

    Cuando se proporciona un PIN incorrecto, el comando debe mostrar un mensaje de error
    y no realizar el depósito.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["depositar", "500", "--pin-input", "9999"])
        assert "PIN incorrecto" in result.output


def test_depositar_monto_negativo(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'depositar' con monto negativo.

    El sistema no debe permitir depósitos con montos negativos.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(
            cajero, ["depositar", "--pin-input", "1234", "--", "-500"]
        )
        assert "Monto debe ser positivo" in result.output


def test_depositar_monto_cero(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'depositar' con monto cero.

    El sistema no debe permitir depósitos con monto cero.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["depositar", "0", "--pin-input", "1234"])
        assert "Monto debe ser positivo" in result.output


def test_depositar_guarda_movimiento(
    runner: CliRunner, temp_estado_file: str
) -> None:
    """
    Prueba que el comando 'depositar' guarda el movimiento en el archivo.

    Después de hacer un depósito, el movimiento debe estar registrado en
    el archivo JSON.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        runner.invoke(cajero, ["depositar", "250.50", "--pin-input", "1234"])

        with open(temp_estado_file, "r") as f:
            estado = json.load(f)

        assert any("Depósito" in mov for mov in estado["movimientos"])


# ==================== TESTS PARA COMANDO retirar ====================


def test_retirar_pin_correcto_fondos_suficientes(
    runner: CliRunner, temp_estado_file: str
) -> None:
    """
    Prueba el comando 'retirar' con PIN correcto y fondos suficientes.

    Cuando se proporciona el PIN correcto y hay fondos suficientes, el comando debe:
    - Mostrar el monto retirado
    - Mostrar el nuevo saldo
    - Guardar el movimiento en el archivo
    """
    with patch("bufalo.modulos.cajero.saldo", 1000.0):
        with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
            result = runner.invoke(cajero, ["retirar", "500", "--pin-input", "1234"])
            assert result.exit_code == 0
            assert "Retirado:" in result.output
            assert "$500" in result.output


def test_retirar_pin_incorrecto(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'retirar' con PIN incorrecto.

    Cuando se proporciona un PIN incorrecto, el comando debe mostrar un
    mensaje de error.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["retirar", "500", "--pin-input", "9999"])
        assert "PIN incorrecto" in result.output


def test_retirar_fondos_insuficientes(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'retirar' con fondos insuficientes.

    Cuando el saldo es menor que el monto a retirar, el sistema debe mostrar un error
    y no permitir el retiro.
    """
    with patch("bufalo.modulos.cajero.saldo", 100.0):
        with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
            result = runner.invoke(cajero, ["retirar", "500", "--pin-input", "1234"])
            assert "Fondos insuficientes" in result.output


def test_retirar_monto_negativo(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'retirar' con monto negativo.

    El sistema no debe permitir retiros con montos negativos.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["retirar", "--pin-input", "1234", "--", "-500"])
        assert "Monto debe ser positivo" in result.output


def test_retirar_monto_cero(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba el comando 'retirar' con monto cero.

    El sistema no debe permitir retiros con monto cero.
    """
    with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
        result = runner.invoke(cajero, ["retirar", "0", "--pin-input", "1234"])
        assert "Monto debe ser positivo" in result.output


def test_retirar_guarda_movimiento(runner: CliRunner, temp_estado_file: str) -> None:
    """
    Prueba que el comando 'retirar' guarda el movimiento en el archivo.

    Después de hacer un retiro, el movimiento debe estar registrado en el archivo JSON.
    """
    with patch("bufalo.modulos.cajero.saldo", 1000.0):
        with patch("bufalo.modulos.cajero.ESTADO_ARCHIVO", temp_estado_file):
            runner.invoke(cajero, ["retirar", "250.50", "--pin-input", "1234"])

            with open(temp_estado_file, "r") as f:
                estado = json.load(f)

            assert any("Retiro" in mov for mov in estado["movimientos"])


# ==================== TESTS PARA COMANDO tipo_cambio ====================


def test_tipo_cambio_pin_correcto(runner: CliRunner) -> None:
    """
    Prueba el comando 'tipo_cambio' con PIN correcto.

    Cuando se proporciona el PIN correcto, el comando debe mostrar los tipos de cambio.
    """
    result = runner.invoke(cajero, ["tipo-cambio", "--pin-input", "1234"])
    assert result.exit_code == 0
    assert "USD -> MXN: $18.50" in result.output
    assert "EUR -> MXN: $20.10" in result.output
    assert "GBP -> MXN: $23.75" in result.output
    assert "Ultima actualizacion: Hoy" in result.output


def test_tipo_cambio_pin_incorrecto(runner: CliRunner) -> None:
    """
    Prueba el comando 'tipo_cambio' con PIN incorrecto.

    Cuando se proporciona un PIN incorrecto, el comando debe mostrar un
    mensaje de error.
    """
    result = runner.invoke(cajero, ["tipo-cambio", "--pin-input", "9999"])
    assert "PIN incorrecto" in result.output


def test_main_entry_point(runner: CliRunner) -> None:
    """
    Prueba la ejecución del módulo como punto de entrada principal.

    Verifica que el grupo 'cajero' se ejecuta correctamente cuando se
    invoca directamente.
    """
    result = runner.invoke(cajero, ["--help"])
    assert result.exit_code == 0
    assert "Cajero automático - PIN default: 1234" in result.output

