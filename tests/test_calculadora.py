"""
Pruebas unitarias para el módulo de calculadora.

Este archivo contiene todas las pruebas para verificar que los comandos
de la calculadora funcionan correctamente. Las pruebas se ejecutan con pytest.

Para ejecutar estas pruebas:
    uv run pytest tests/test_calculadora.py -v
"""

# Importamos CliRunner de Click, que nos permite probar comandos CLI
# sin tener que ejecutarlos en la terminal real
from click.testing import CliRunner

# Importamos el grupo de comandos 'calculadora' que vamos a probar
from bufalo.modulos.calculadora import calculadora


def test_suma_multiple_numbers() -> None:
    """
    Prueba que el comando 'suma' funciona correctamente con múltiples números.

    Esta prueba verifica que podemos sumar varios números a la vez.
    Ejemplo: suma 1 2 3 4 = 10
    """
    # CliRunner es una herramienta que simula la ejecución de comandos CLI
    runner = CliRunner()

    # Invocamos el comando 'suma' con los argumentos ["suma", "1", "2", "3", "4"]
    # Es como escribir en la terminal: bufalo calculadora suma 1 2 3 4
    result = runner.invoke(calculadora, ["suma", "1", "2", "3", "4"])

    # Verificamos que el comando terminó exitosamente (exit_code 0 significa éxito)
    assert result.exit_code == 0

    # Verificamos que el resultado en la salida sea correcto
    assert "Resultado: 10.0" in result.output


def test_suma_single_number() -> None:
    """
    Prueba que el comando 'suma' funciona con un solo número.

    Cuando sumamos un solo número, el resultado debe ser ese mismo número.
    Ejemplo: suma 5 = 5
    """
    runner = CliRunner()

    # Invocamos suma con un solo número
    result = runner.invoke(calculadora, ["suma", "5"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 5.0
    assert "Resultado: 5.0" in result.output


def test_suma_no_numbers() -> None:
    """
    Prueba que el comando 'suma' funciona sin argumentos.

    Cuando no pasamos ningún número, la suma debe ser 0.
    Ejemplo: suma = 0

    Nota: Python devuelve 0 (entero) en lugar de 0.0 (decimal) cuando
    la lista está vacía, por eso buscamos "Resultado: 0" sin el .0
    """
    runner = CliRunner()

    # Invocamos suma sin ningún número
    result = runner.invoke(calculadora, ["suma"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 0 (sin decimales porque la lista está vacía)
    assert "Resultado: 0" in result.output


def test_suma_negative_numbers() -> None:
    """
    Prueba que el comando 'suma' funciona con números negativos.

    Los números negativos requieren un separador especial '--' antes de ellos.
    Esto es porque Click (la librería CLI) interpreta -1 como una opción/flag.

    Ejemplo: suma -- -1 -2 -3 = -6

    El '--' le dice a Click: "todo lo que viene después son argumentos, no opciones"
    """
    runner = CliRunner()

    # Nota el uso de "--" antes de los números negativos
    # Sin el "--", Click pensaría que -1 es una opción como --help
    result = runner.invoke(calculadora, ["suma", "--", "-1", "-2", "-3"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser -6.0
    assert "Resultado: -6.0" in result.output


def test_resta_positive_result() -> None:
    """
    Prueba que el comando 'resta' funciona cuando el resultado es positivo.

    Ejemplo: resta 10 3 = 7
    """
    runner = CliRunner()

    # Restamos 3 de 10
    result = runner.invoke(calculadora, ["resta", "10", "3"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 7.0
    assert "Resultado: 7.0" in result.output


def test_resta_negative_result() -> None:
    """
    Prueba que el comando 'resta' funciona cuando el resultado es negativo.

    Ejemplo: resta 3 10 = -7
    """
    runner = CliRunner()

    # Restamos 10 de 3, lo que da un número negativo
    result = runner.invoke(calculadora, ["resta", "3", "10"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser -7.0
    assert "Resultado: -7.0" in result.output


def test_resta_zero_result() -> None:
    """
    Prueba que el comando 'resta' funciona cuando el resultado es cero.

    Cuando restamos un número de sí mismo, el resultado es 0.
    Ejemplo: resta 5 5 = 0
    """
    runner = CliRunner()

    # Restamos 5 de 5
    result = runner.invoke(calculadora, ["resta", "5", "5"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 0.0
    assert "Resultado: 0.0" in result.output


def test_multiplica_positive_numbers() -> None:
    """
    Prueba que el comando 'multiplica' funciona con números positivos.

    Ejemplo: multiplica 3 4 = 12
    """
    runner = CliRunner()

    # Multiplicamos 3 por 4
    result = runner.invoke(calculadora, ["multiplica", "3", "4"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 12.0
    assert "Resultado: 12.0" in result.output


def test_multiplica_by_zero() -> None:
    """
    Prueba que el comando 'multiplica' funciona cuando multiplicamos por cero.

    Cualquier número multiplicado por 0 es 0.
    Ejemplo: multiplica 5 0 = 0
    """
    runner = CliRunner()

    # Multiplicamos 5 por 0
    result = runner.invoke(calculadora, ["multiplica", "5", "0"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 0.0
    assert "Resultado: 0.0" in result.output


def test_multiplica_negative_numbers() -> None:
    """
    Prueba que el comando 'multiplica' funciona con números negativos.

    Cuando multiplicamos un número negativo por uno positivo, el resultado es negativo.
    Ejemplo: multiplica -2 3 = -6

    Nota: Usamos '--' antes del número negativo por la misma razón que en suma.
    """
    runner = CliRunner()

    # Multiplicamos -2 por 3, usando "--" antes del número negativo
    result = runner.invoke(calculadora, ["multiplica", "--", "-2", "3"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser -6.0
    assert "Resultado: -6.0" in result.output


def test_divide_normal() -> None:
    """
    Prueba que el comando 'divide' funciona con una división normal.

    Ejemplo: divide 10 2 = 5
    """
    runner = CliRunner()

    # Dividimos 10 entre 2
    result = runner.invoke(calculadora, ["divide", "10", "2"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 5.0
    assert "Resultado: 5.0" in result.output


def test_divide_by_zero() -> None:
    """
    Prueba que el comando 'divide' maneja correctamente la división por cero.

    Dividir por cero es matemáticamente imposible, así que el programa
    debe mostrar un mensaje de error en lugar de fallar.

    Ejemplo: divide 10 0 = Error
    """
    runner = CliRunner()

    # Intentamos dividir 10 entre 0
    result = runner.invoke(calculadora, ["divide", "10", "0"])

    # El comando debe terminar exitosamente (no debe crashear)
    assert result.exit_code == 0

    # Debe mostrar un mensaje de error apropiado
    assert "Error: No se puede dividir por cero." in result.output


def test_divide_negative_numbers() -> None:
    """
    Prueba que el comando 'divide' funciona con números negativos.

    Cuando dividimos un número negativo entre uno positivo, el resultado es negativo.
    Ejemplo: divide -10 2 = -5

    Nota: Usamos '--' antes del número negativo.
    """
    runner = CliRunner()

    # Dividimos -10 entre 2, usando "--" antes del número negativo
    result = runner.invoke(calculadora, ["divide", "--", "-10", "2"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser -5.0
    assert "Resultado: -5.0" in result.output


def test_divide_zero_by_number() -> None:
    """
    Prueba que el comando 'divide' funciona cuando dividimos cero entre un número.

    Cero dividido entre cualquier número (excepto cero) es siempre cero.
    Ejemplo: divide 0 5 = 0
    """
    runner = CliRunner()

    # Dividimos 0 entre 5
    result = runner.invoke(calculadora, ["divide", "0", "5"])

    # El comando debe terminar exitosamente
    assert result.exit_code == 0

    # El resultado debe ser 0.0
    assert "Resultado: 0.0" in result.output
