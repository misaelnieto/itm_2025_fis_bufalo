"""
Módulo de pruebas para el contador de palabras.

Contiene pruebas unitarias para validar el comportamiento de los comandos
para contar y analizar palabras en textos.
"""
# Importamos CliRunner de Click, que nos permite probar comandos CLI
# sin tener que ejecutarlos en la terminal real
import pytest
from click.testing import CliRunner

# Importamos el grupo de comandos 'palabras' que vamos a probar

from bufalo.modulos.contadorPalabras import palabras


@pytest.fixture
def runner() -> CliRunner:
    """
    Crea un ejecutor de CLI de Click para pruebas.
    
    Returns:
        CliRunner: Instancia para invocar comandos CLI sin necesidad de terminal real.
    """
    return CliRunner()


def test_contar_palabras_simple(runner: CliRunner) -> None:
    """
    Verifica que el comando 'contar' cuenta correctamente palabras simples.
    
    Prueba que el texto "hola mundo esto es una prueba" contiene exactamente 6 palabras.
    
    Args:
        runner: Fixture que proporciona el ejecutor de CLI.
    """
    resultado = runner.invoke(
        palabras,
        ["contar", "hola mundo esto es una prueba"],
    )
    assert resultado.exit_code == 0
    # "hola mundo esto es una prueba" = 6 palabras
    assert resultado.output.strip() == "6"


def test_top_palabras(runner: CliRunner) -> None:
    """
    Verifica que el comando 'top' ordena correctamente palabras por frecuencia.
    
    Prueba que con el texto "hola hola mundo mundo mundo", al solicitar las 2 palabras
    más frecuentes, se obtiene: "mundo: 3" y "hola: 2" en ese orden.
    
    Args:
        runner: Fixture que proporciona el ejecutor de CLI.
    """
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
