import pytest, click
from click.testing import CliRunner
from bufalo.modulos.tic_tac_toe import tictactoe, check_win, simple_ai, Game, Board

def test_core():
    assert check_win(["X"]*3 + [" "]*6, "X") is True
    assert simple_ai(["O","O"," "," "," "," "," "," "," "], "O") == 2
    assert simple_ai(["X"]*9, "O") == -1
    b = Board(); assert "|1|" in b.display()
    g = Game("X"); assert g.process(0) is True; assert g.process(0) is False

def test_cli_flows(monkeypatch):
    runner = CliRunner()
    # Caso 1: Jugador gana (X)
    monkeypatch.setattr("click.prompt", lambda msg, **k: "X" if "X/O" in msg else 1 if "Pos" in msg else 2 if g.curr=="O" else 3)
    runner.invoke(tictactoe, ["jugar"], input="X\n1\n2\n3\n")
    
    # Caso 2: IA gana (Jugador elige O y pierde rápido)
    r2 = iter(["O", 9, 8, 7])
    monkeypatch.setattr("click.prompt", lambda *a, **k: next(r2))
    runner.invoke(tictactoe, ["jugar"])
    
    # Caso 3: Empate/Error
    def mock_err(*a, **k): raise RuntimeError()
    monkeypatch.setattr("click.prompt", mock_err)
    res = runner.invoke(tictactoe, ["jugar"])
    assert "Out:RuntimeError" in res.output

def test_meta():
    runner = CliRunner()
    runner.invoke(tictactoe)
    runner.invoke(tictactoe, ["--help"])