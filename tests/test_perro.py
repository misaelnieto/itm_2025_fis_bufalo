from click.testing import CliRunner

from bufalo.modulos.perro import perro


def test_perro_bailando_muestra_una_pose() -> None:
    runner = CliRunner()
    result = runner.invoke(perro, ["bailar"])
    assert result.exit_code == 0
    assert (
        len(result.output) > 50
    )  
    assert "(\\_/)" in result.output
    assert " ( o.o )  " in result.output
    assert " ( ^.^ )  " in result.output
