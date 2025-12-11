import json
import tempfile

from click.testing import CliRunner

from bufalo.modulos.follows import francisco


def test_myfollows_option_real_data() -> None:
    """Prueba completa de --myfollows con datos simulados."""
    runner = CliRunner()

    followers_data = {
        "string_list_data": [{"value": "juan"}, {"value": "maria"}, {"value": "pedro"}]
    }
    following_data = {
        "relationships_following": [
            {"title": "juan"},
            {"title": "ana"},
            {"title": "pedro"},
        ]
    }

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(francisco, ["comparar", "--myfollows", f1.name, f2.name])

    assert result.exit_code == 0
    assert "ana" in result.output
    assert "Personas que sigues pero NO te siguen" in result.output


def test_myfollowers_option_real_data() -> None:
    """Prueba completa de --myfollowers con datos simulados."""
    runner = CliRunner()

    followers_data = {
        "string_list_data": [
            {"value": "juan"},
            {"value": "maria"},
            {"value": "pedro"},
            {"value": "lucia"},
        ]
    }
    following_data = {
        "relationships_following": [
            {"title": "juan"},
            {"title": "pedro"},
            {"title": "ana"},
        ]
    }

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(
            francisco, ["comparar", "--myfollowers", f1.name, f2.name]
        )

    assert result.exit_code == 0
    assert "maria" in result.output
    assert "lucia" in result.output
    assert "Seguidores que NO sigues de vuelta" in result.output


def test_comparar_without_options() -> None:
    """Prueba cuando no se pasa ninguna opción (--myfollows ni --myfollowers)."""
    runner = CliRunner()

    followers_data = {"string_list_data": [{"value": "juan"}, {"value": "maria"}]}
    following_data = {
        "relationships_following": [{"title": "juan"}, {"title": "pedro"}]
    }

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(francisco, ["comparar", f1.name, f2.name])

    assert result.exit_code == 0
    assert "Debes especificar --myfollows o --myfollowers" in result.output


# 🔥 Tests adicionales para cobertura total


def test_lista_como_followers_data() -> None:
    """Cubre el caso donde followers_data es una lista en vez de dict."""
    runner = CliRunner()

    followers_data = [
        {"string_list_data": [{"value": "ana"}]},
        {"string_list_data": [{"value": "juan"}]},
    ]
    following_data = {"relationships_following": [{"title": "ana"}, {"title": "juan"}]}

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(
            francisco,
            ["comparar", "--myfollowers", f1.name, f2.name],
        )

    assert result.exit_code == 0
    assert "✅ Sigues a todos tus seguidores" in result.output


def test_todos_me_siguen() -> None:
    """Cubre el caso donde todos los que sigues también te siguen."""
    runner = CliRunner()

    followers_data = {"string_list_data": [{"value": "ana"}, {"value": "juan"}]}
    following_data = {"relationships_following": [{"title": "ana"}, {"title": "juan"}]}

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(francisco, ["comparar", "--myfollows", f1.name, f2.name])

    assert result.exit_code == 0
    assert "✅ Todos los que sigues también te siguen" in result.output


def test_todos_los_sigo() -> None:
    """Cubre el caso donde todos los seguidores también los sigues."""
    runner = CliRunner()

    followers_data = {"string_list_data": [{"value": "ana"}, {"value": "juan"}]}
    following_data = {"relationships_following": [{"title": "ana"}, {"title": "juan"}]}

    with (
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f1,
        tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as f2,
    ):
        json.dump(followers_data, f1)
        json.dump(following_data, f2)
        f1.seek(0)
        f2.seek(0)

        result = runner.invoke(
            francisco,
            ["comparar", "--myfollowers", f1.name, f2.name],
        )

    assert result.exit_code == 0
    assert "✅ Sigues a todos tus seguidores" in result.output


def test_followers_data_unexpected_type(tmp_path):
    """Cubre el caso donde followers_data no es dict ni list (ejemplo: string)."""
    runner = CliRunner()
    f1 = tmp_path / "followers.json"
    f2 = tmp_path / "following.json"

    # followers_data como string para forzar el else
    f1.write_text(json.dumps("valor_invalido"), encoding="utf-8")
    f2.write_text(json.dumps({"relationships_following": []}), encoding="utf-8")

    result = runner.invoke(francisco, ["comparar", "--myfollowers", str(f1), str(f2)])
    assert result.exit_code == 0
    assert "✅ Sigues a todos tus seguidores" in result.output
