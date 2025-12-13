from click.testing import CliRunner

from bufalo.modulos.tic_tac_toe import Board, Game, check_win, simple_ai, tictactoe


def test_core():
    assert check_win(["X"] * 3 + [" "] * 6, "X") is True
    assert simple_ai(["O", "O", " ", " ", " ", " ", " ", " ", " "], "O") == 2
    assert simple_ai(["X"] * 9, "O") == -1
    b = Board()
    assert "|1|" in b.display()
    g = Game("X")
    assert g.process(0) is True
    assert g.process(0) is False


def test_cli_flows(monkeypatch):
    runner = CliRunner()
    # Caso 1: Jugador gana
    r1 = iter(["X", 1, 2, 3, 4, 5])
    monkeypatch.setattr("click.prompt", lambda *a, **k: next(r1))
    runner.invoke(tictactoe, ["jugar"])

    # Caso 2: IA gana
    r2 = iter(["O", 9, 8, 7])
    monkeypatch.setattr("click.prompt", lambda *a, **k: next(r2))
    runner.invoke(tictactoe, ["jugar"])

    # Caso 3: Error
    def mock_err(*a, **k):
        raise RuntimeError()

    monkeypatch.setattr("click.prompt", mock_err)
    res = runner.invoke(tictactoe, ["jugar"])
    assert "Out:RuntimeError" in res.output


def test_meta():
    runner = CliRunner()
    runner.invoke(tictactoe)
    runner.invoke(tictactoe, ["--help"])
