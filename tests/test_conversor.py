# tests/test_conversor.py

import pytest
from click.testing import CliRunner

# Intentamos importar el CLI principal. El módulo conversor
# se cargará automáticamente si está en src/bufalo/modulos/
from src.bufalo.cli import main as cli


# Creamos una instancia de CliRunner para ejecutar los comandos
@pytest.fixture
def runner():
    """Fixture para obtener una instancia de CliRunner."""
    return CliRunner()


def test_conversion_celsius_a_fahrenheit_exitoso(runner: CliRunner):
    """
    PRUEBA 1:
    Verifica que el comando 'c-a-f' convierta correctamente
    25 grados Celsius a 77.0 grados Fahrenheit.
    """
    # ARRANGE: Definimos el valor de entrada y el resultado esperado.
    valor_celsius = 25.0
    resultado_esperado = "77.0"  # Click siempre devuelve texto.

    # ACT: Ejecutamos el comando CLI.
    # El comando es: bufalo conversor c-a-f 25
    result = runner.invoke(cli, ["conversor", "c-a-f", str(valor_celsius)])

    # ASSERT: Verificamos el código de salida y el resultado.
    assert result.exit_code == 0
    # Quitamos espacios o saltos de línea y verificamos la salida.
    assert result.output.strip() == resultado_esperado


def test_conversion_fahrenheit_a_celsius_exitoso(runner: CliRunner):
    """
    PRUEBA 2:
    Verifica que el comando 'f-a-c' convierta correctamente
    32 grados Fahrenheit a 0.0 grados Celsius.
    """
    # ARRANGE: Definimos el valor de entrada y el resultado esperado.
    valor_fahrenheit = 32.0
    resultado_esperado = "0.0"

    # ACT: Ejecutamos el comando CLI.
    # El comando es: bufalo conversor f-a-c 32
    result = runner.invoke(cli, ["conversor", "f-a-c", str(valor_fahrenheit)])

    # ASSERT: Verificamos el código de salida y el resultado.
    assert result.exit_code == 0
    assert result.output.strip() == resultado_esperado


# Tarea: Añadir más pruebas (ej. números negativos, punto de congelación)
# Tarea: Ejecuta 'uv run pytest' y verifica que estas pruebas FALLEN.
