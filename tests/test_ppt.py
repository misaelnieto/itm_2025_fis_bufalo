from click.testing import CliRunner

from bufalo.cli import main


def test_ppt_gana(monkeypatch):
    # Forzamos que la CPU elija "tijeras" => jugador "piedra" gana.
    monkeypatch.setattr("bufalo.modulos.ppt.random.choice", lambda opts: "tijeras")
    runner = CliRunner()
    result = runner.invoke(main, ["ppt", "jugar", "piedra"])
    assert result.exit_code == 0
    assert "Tú: piedra" in result.output
    assert "CPU: tijeras" in result.output
    assert "Ganaste" in result.output


def test_ppt_pierde(monkeypatch):
    # Forzamos que la CPU elija "papel" => jugador "piedra" pierde.
    monkeypatch.setattr("bufalo.modulos.ppt.random.choice", lambda opts: "papel")
    runner = CliRunner()
    result = runner.invoke(main, ["ppt", "jugar", "piedra"])
    assert result.exit_code == 0
    assert "Tú: piedra" in result.output
    assert "CPU: papel" in result.output
    assert "Perdiste" in result.output


def test_ppt_empate(monkeypatch):
    # Forzamos que la CPU elija "piedra" => empate.
    monkeypatch.setattr("bufalo.modulos.ppt.random.choice", lambda opts: "piedra")
    runner = CliRunner()
    result = runner.invoke(main, ["ppt", "jugar", "piedra"])
    assert result.exit_code == 0
    assert "Tú: piedra" in result.output
    assert "CPU: piedra" in result.output
    assert "Empate" in result.output
