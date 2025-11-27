from click.testing import CliRunner

from bufalo.cli import main


def test_main() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "🦬  Bufalo 🦬" in result.output


def test_autodiscovery_registers_calculadora() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "calculadora" in result.output
