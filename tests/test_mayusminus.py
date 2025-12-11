from click.testing import CliRunner

from bufalo.modulos.mayusminus import mayusminus


def test_convertir_mayus() -> None:
    """Prueba que convierte el texto a mayúsculas."""
    # CliRunner es una herramienta que simula la ejecución de comandos CLI
    runner = CliRunner()
    # Para poder invocar el comando mayuscula con agumento de string
    result = runner.invoke(mayusminus, ["mayuscula", "ola de saludo"])
    assert result.exit_code == 0
    # Suponiendo que entra "ola de saludo", debe salir "OLA DE SALUDO"
    assert "OLA DE SALUDO" in result.output


def test_convertir_minus() -> None:
    """Prueba que convierte el texto a minúsculas"""
    runner = CliRunner()
    # Para poder invocar ahora el comando munuscula con argumento un string
    result = runner.invoke(mayusminus, ["minuscula", "OLA DE SALUDO"])
    assert result.exit_code == 0
    # Suponiendo que entra "OLA DE SALUDO", debe salir "ola de saludo"
    assert "ola de saludo" in result.output


def test_convertir_toascii() -> None:
    """Prueba que convierte un texto (string) a códigos ASCII."""
    runner = CliRunner()
    # Para poder invocar el comando toascii con argumento un string
    result = runner.invoke(mayusminus, ["toascii", "ABC"])
    assert result.exit_code == 0
    # Suponiendo que entra "ABC", debe salir "65 66 67"
    assert "65 66 67" in result.output


def test_convertir_fromascii() -> None:
    """Prueba que convierte códigos ASCII a texto (string)."""
    runner = CliRunner()
    # Para poder invocar el comando fromascii con argumento integers
    #  separados por espacio
    result = runner.invoke(mayusminus, ["fromascii", "65 66 67"])
    assert result.exit_code == 0
    # Suponiendo que entra "65 66 67", debe salir "ABC"
    assert "ABC" in result.output


def test_fromascii_error() -> None:
    """Prueba que fromascii falla con entrada inválida (no numérica)."""
    runner = CliRunner()
    # Proporcionamos un token no numérico para forzar ValueError
    result = runner.invoke(mayusminus, ["fromascii", "65 x 67"])
    # Debe fallar (exit code distinto de 0) y mostrar mensaje de error
    assert result.exit_code != 0
    assert "Entrada inválida" in result.output
