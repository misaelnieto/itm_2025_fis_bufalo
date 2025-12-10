from click.testing import CliRunner
import pytest
from bufalo.modulos.contadorPalabras import palabras

@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

def test_contar_palabras_simple(runner: CliRunner) -> None:
    resultado = runner.invoke(
        palabras,
        ["contar", "hola mundo esto es una prueba"],
    )
    assert resultado.exit_code == 0
    # "hola mundo esto es una prueba" = 6 palabras
    assert resultado.output.strip() == "6"

def test_top_palabras(runner: CliRunner) -> None:
    texto = "hola hola mundo mundo mundo"
    resultado = runner.invoke(
        palabras,
        ["top", texto, "--top", "2"],
    )
    assert resultado.exit_code == 0

    salida = resultado.output.strip().splitlines()
    # Esperamos:
    # mundo: 3
    # hola: 2
    assert "mundo: 3" in salida[0]
    assert "hola: 2" in salida[1]

