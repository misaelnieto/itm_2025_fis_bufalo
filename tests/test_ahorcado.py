import builtins
import random

from click.testing import CliRunner

from bufalo.modulos.ahorcado import ahorcado


def test_comando_existe() -> None:
    """Verifica que el grupo ahorcado pueda ejecutarse."""
    runner = CliRunner()
    result = runner.invoke(ahorcado)
    assert result.exit_code == 0


def test_ganar_partida(monkeypatch) -> None:
    """
    Simula una partida ganada.

    - Se fija la palabra que devuelve random.choice
    - Se simula que el usuario escribe todas las letras correctas
    """

    # Forzamos palabra = "python"
    monkeypatch.setattr(random, "choice", lambda x: "python")

    # Simulamos entradas del usuario (p, y, t, h, o, n)

    inputs = iter(["p", "y", "t", "h", "o", "n"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    runner = CliRunner()
    result = runner.invoke(ahorcado, ["jugar"])

    assert result.exit_code == 0
    assert "¡Ganaste! La palabra era: python" in result.output


def test_perder_partida(monkeypatch) -> None:
    """
    Simula perder la partida.
    Elegimos una palabra fija y damos solo letras incorrectas.
    """

    monkeypatch.setattr(random, "choice", lambda x: "raton")

    # 6 intentos fallidos
    inputs = iter(["x", "z", "y", "w", "v", "q"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    runner = CliRunner()
    result = runner.invoke(ahorcado, ["jugar"])

    assert result.exit_code == 0
    assert "Perdiste... la palabra era: raton" in result.output


def test_repite_letra(monkeypatch) -> None:
    """
    Si el usuario llega a repetir la letra,
    el juego debe avisar "Ya usaste esa letra".
    """

    monkeypatch.setattr(random, "choice", lambda x: "raton")

    # r (bien), r de nuevo (mensaje), x (fallo), ...
    inputs = iter(["r", "r", "x", "y", "z", "w", "v"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    runner = CliRunner()
    result = runner.invoke(ahorcado, ["jugar"])

    assert "Ya usaste esa letra" in result.output
