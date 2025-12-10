from click.testing import CliRunner

from bufalo.modulos.temperatura import temperatura


def test_celsius_a_fahrenheit():
    runner = CliRunner()
    result = runner.invoke(temperatura, ["acelsius", "0"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "32.0"


def test_fahrenheit_a_celsius():
    runner = CliRunner()
    result = runner.invoke(temperatura, ["afahrenheit", "32"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "0.0"
