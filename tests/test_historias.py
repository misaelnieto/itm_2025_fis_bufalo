from unittest.mock import patch  # Necesario para controlar random.choice

from click.testing import CliRunner  # Necesario para probar comandos CLI

from src.bufalo.modulos.historias import generar_historia, historias


def test_generar_historia_devuelve_string():
    historia = generar_historia()
    assert isinstance(historia, str)
    assert len(historia) > 0


# 1. Prueba para el 100% de Cobertura de la Lógica (generar_historia)
@patch("random.choice")
def test_generar_historia_formato_completo(mock_choice):
    """
    Verifica que la funcion construye la cadena con el formato correcto.
    Usa mocking para simular random.choice.
    """
    # Define los valores de retorno para los 3 random.choice
    mock_choice.side_effect = ["Un Gato", "en Marte", "quería comer pescado"]

    historia_fija = generar_historia()

    expected_result = "Había una vez Un Gato que vivía en Marte y quería comer pescado."

    # Verifica que la historia generada coincide con el formato esperado.
    assert historia_fija == expected_result
    # Assert: Opcional, verifica que random.choice fue llamado 3 veces.
    assert mock_choice.call_count == 3


# 2. Prueba para el 100% de Cobertura del CLI (Comandos click)
def test_comando_generar_funciona_y_llama_logica():
    """
    Verifica que el comando CLI 'historias generar' se ejecuta correctamente
    (cubre líneas click).
    """
    runner = CliRunner()

    # Usa patch para simular la salida de la funcion logica
    with patch(
        "src.bufalo.modulos.historias.generar_historia",
        return_value="Historia CLI de prueba.",
    ):
        # Llama al comando 'generar'
        result = runner.invoke(historias, ["generar"])

        # Assert: El codigo de salida debe ser 0 (exito)
        assert result.exit_code == 0
        # La salida de la terminal contiene el resultado simulado.
        assert "Historia CLI de prueba." in result.output
