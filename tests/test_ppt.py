from click.testing import CliRunner

from bufalo.cli import main


def test_ppt_gana():
    runner = CliRunner()
    resultado = runner.invoke(main, ["ppt", "jugar", "piedra", "tijeras"])
    assert "Ganaste" in resultado.output


def test_ppt_pierde():
    runner = CliRunner()
    resultado = runner.invoke(main, ["ppt", "jugar", "piedra", "papel"])
    assert "Perdiste" in resultado.output


def test_ppt_empate():
    runner = CliRunner()
    resultado = runner.invoke(main, ["ppt", "jugar", "piedra", "piedra"])
    assert "Empate" in resultado.output
