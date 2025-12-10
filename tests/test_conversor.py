from click.testing import CliRunner

from bufalo.modulos.conversor import conversor


def test_convertir_metros_a_kilometros() -> None:
    runner = CliRunner()
    result = runner.invoke(conversor, ["convertir", "1000", "m", "km"])

    assert result.exit_code == 0
    assert "Resultado: 1.0" in result.output


def test_convertir_kilometros_a_metros() -> None:
    runner = CliRunner()
    result = runner.invoke(conversor, ["convertir", "1.5", "km", "m"])

    assert result.exit_code == 0
    assert "Resultado: 1500.0" in result.output


def test_convertir_centimetros_a_metros() -> None:
    runner = CliRunner()
    result = runner.invoke(conversor, ["convertir", "250", "cm", "m"])

    assert result.exit_code == 0
    assert "Resultado: 2.5" in result.output


def test_unidad_no_valida() -> None:
    runner = CliRunner()
    result = runner.invoke(conversor, ["convertir", "10", "mm", "m"])

    # Debe fallar porque "mm" no es una unidad soportada
    assert result.exit_code != 0
    assert "Error: Unidad no válida" in result.output
    # El orden de las unidades debe coincidir con el dict UNIDADES
    assert "km, m, cm" in result.output
