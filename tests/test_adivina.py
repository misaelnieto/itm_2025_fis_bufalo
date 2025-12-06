from click.testing import CliRunner
from bufalo.modulos.adivina import adivina, evaluar_intento
# ---------------------------
# PRUEBAS UNITARIAS
# ---------------------------


def test_evaluar_intento_gana():
    assert evaluar_intento(50, 50) == "ganaste"


def test_evaluar_intento_muy_bajo():
    assert evaluar_intento(50, 10) == "muy bajo"


def test_evaluar_intento_muy_alto():
    assert evaluar_intento(50, 90) == "muy alto"


# ---------------------------
# PRUEBAS CLI
# ---------------------------


def test_cli_jugar():
    runner = CliRunner()

    # Simulamos 3 intentos
    result = runner.invoke(adivina, ["jugar"], input="10\n50\n70\n")

    # Verificaciones mínimas necesarias
    assert "Adivina un número entre 1 y 100" in result.output
    assert "Intento 1" in result.output
    assert "Intento 2" in result.output
    assert "Intento 3" in result.output
    assert result.exit_code == 0


def test_cli_dificil():
    runner = CliRunner()

    # Simulamos 3 intentos
    result = runner.invoke(adivina, ["dificil"], input="100\n500\n900\n")

    # Verificaciones mínimas necesarias
    assert "Modo difícil" in result.output
    assert "Intento 1" in result.output
    assert "Intento 2" in result.output
    assert "Intento 3" in result.output
    assert result.exit_code == 0
