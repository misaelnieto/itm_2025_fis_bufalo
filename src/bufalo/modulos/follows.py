import click
import json

@click.group()
def francisco():
    """Comandos de análisis de seguidores"""
    pass

@francisco.command()
@click.option("--myfollows", is_flag=True, help="Muestra a los que sigo y no me siguen")
@click.option("--myfollowers", is_flag=True, help="Muestra a los que me siguen pero no los sigo")
@click.argument("followers_path")
@click.argument("following_path")
def comparar(myfollows, myfollowers, followers_path, following_path):
    """Compara seguidores y seguidos desde dos archivos JSON"""
    with open(followers_path, "r", encoding="utf-8") as f:
        followers_data = json.load(f)
    with open(following_path, "r", encoding="utf-8") as f:
        following_data = json.load(f)

    if isinstance(followers_data, dict):
        followers = [item["value"] for item in followers_data.get("string_list_data", [])]
    elif isinstance(followers_data, list):
        followers = [item["string_list_data"][0]["value"] for item in followers_data]
    else:
        followers = []

    following = [entry["title"] for entry in following_data.get("relationships_following", [])]

    no_sigo_de_vuelta = [f for f in followers if f not in following]
    no_me_siguen = [f for f in following if f not in followers]

    if myfollows:
        click.echo("=== Personas que sigues pero NO te siguen ===")
        if no_me_siguen:
            for f in no_me_siguen:
                click.echo(f" - " + f)
        else:
            click.echo("  ✅ Todos los que sigues también te siguen")

    elif myfollowers:
        click.echo("=== Seguidores que NO sigues de vuelta ===")
        if no_sigo_de_vuelta:
            for f in no_sigo_de_vuelta:
                click.echo(f" - " + f)
        else:
            click.echo("  ✅ Sigues a todos tus seguidores")
