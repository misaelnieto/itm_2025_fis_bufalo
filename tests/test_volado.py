from unittest.mock import patch

import pytest
from click.testing import CliRunner

from bufalo.modulos.volado import jugar_volado, tirar_moneda, volado

### 1. Pruebas de Lógica Pura (tirar_moneda) ###


def test_tirar_moneda_resultado_valido():
    """Prueba que el resultado siempre sea 'aguila' o 'sello'."""
    resultado = tirar_moneda()
    assert resultado in ("aguila", "sello")


@patch("bufalo.modulos.volado.random.choice")
def test_tirar_moneda_predecible_aguila(mock_choice):
    """Fuerza la tirada a 'aguila' para asegurar la salida esperada."""
    mock_choice.return_value = "aguila"
    assert tirar_moneda() == "aguila"


@patch("bufalo.modulos.volado.random.choice")
def test_tirar_moneda_predecible_sello(mock_choice):
    """Fuerza la tirada a 'sello' para asegurar la salida esperada."""
    mock_choice.return_value = "sello"
    assert tirar_moneda() == "sello"


### 2. Pruebas de Lógica Pura (jugar_volado) ###


def test_jugar_volado_gana():
    """Prueba que el jugador gana cuando la apuesta y el resultado coinciden."""
    apuesta = "aguila"
    resultado = "aguila"
    assert jugar_volado(apuesta, resultado)


def test_jugar_volado_pierde():
    """Prueba que el jugador pierde cuando la apuesta y el resultado NO coinciden."""
    apuesta = "sello"
    resultado = "aguila"
    assert not jugar_volado(apuesta, resultado)


def test_jugar_volado_apuesta_invalida():
    """Prueba que una apuesta diferente a 'aguila' o 'sello' lance ValueError."""
    with pytest.raises(ValueError):
        jugar_volado("gato", "aguila")


def test_jugar_volado_resultado_invalido():
    """Prueba que un resultado de moneda inesperado lance ValueError."""
    with pytest.raises(ValueError):
        jugar_volado("aguila", "sol")


### 3. Pruebas de Interfaz CLI (volado command) ###


def test_comando_volado_muestra_ayuda():
    """
    Prueba que el grupo 'volado' muestre la ayuda correctamente
    y el subcomando 'lanzar'.
    """
    runner = CliRunner()
    result = runner.invoke(volado, ["--help"])  # Invocamos la ayuda del GRUPO
    assert result.exit_code == 0
    assert "Juega un volado" in result.output
    # Buscamos el subcomando 'lanzar'
    assert "lanzar" in result.output


@patch("bufalo.modulos.volado.tirar_moneda", return_value="aguila")
def test_comando_volado_gana(mock_tirar):
    """Prueba que el comando ejecute el juego y reporte una victoria."""
    runner = CliRunner()
    # Invocamos 'lanzar' como subcomando con el argumento 'aguila'
    result = runner.invoke(volado, ["lanzar", "aguila"])
    assert result.exit_code == 0
    assert "Resultado: AGUILA" in result.output
    assert "¡HAS GANADO EL VOLADO!" in result.output


@patch("bufalo.modulos.volado.tirar_moneda", return_value="sello")
def test_comando_volado_pierde(mock_tirar):
    """Prueba que el comando ejecute el juego y reporte una derrota."""
    runner = CliRunner()
    # Invocamos 'lanzar' como subcomando con el argumento 'aguila'
    result = runner.invoke(volado, ["lanzar", "aguila"])
    assert result.exit_code == 0
    assert "Resultado: SELLO" in result.output
    assert "¡HAS PERDIDO EL VOLADO!" in result.output


def test_comando_volado_apuesta_invalida_cli():
    """Prueba que click intercepte una apuesta inválida con un código de error."""
    runner = CliRunner()
    # Invocamos 'lanzar' con el argumento inválido 'gato'
    result = runner.invoke(volado, ["lanzar", "gato"])
    assert result.exit_code != 0
    # El mensaje de error es el mismo para el subcomando
    assert "Invalid value for '{aguila|sello}'" in result.output
