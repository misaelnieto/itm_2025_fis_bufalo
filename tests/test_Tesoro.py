import unittest.mock
import io
import sys
import pytest

from src.bufalo.modulos.Tesoro import caza_del_tesoro


@pytest.fixture
def capture_output():
    new_stdout = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = new_stdout
    yield new_stdout
    sys.stdout = old_stdout


@unittest.mock.patch("random.randint")
@unittest.mock.patch("builtins.input")
def test_ganar_en_el_primer_intento(mock_input, mock_random_randint, capture_output):
    mock_random_randint.side_effect = [0, 1]
    mock_input.side_effect = ["1,2"]
    caza_del_tesoro()
    output = capture_output.getvalue()
    assert "¡Felicidades! Encontraste el tesoro" in output
    assert "💰" in output


@unittest.mock.patch("random.randint")
@unittest.mock.patch("builtins.input")
def test_perder_por_agotar_intentos(mock_input, mock_random_randint, capture_output):
    mock_random_randint.side_effect = [2, 2]
    mock_input.side_effect = ["1,1", "1,2", "1,3", "2,1", "2,3"]
    caza_del_tesoro()
    output = capture_output.getvalue()
    assert "--- ¡Fin del juego! ---" in output
    assert "El tesoro estaba en la Fila 3, Columna 3." in output
    assert output.count("X") == 5
