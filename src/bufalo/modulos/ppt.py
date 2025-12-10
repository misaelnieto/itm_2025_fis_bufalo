import click

OPCIONES = ["piedra", "papel", "tijeras"]


@click.group()
def ppt():
    """Juego de Piedra, Papel o Tijeras"""
    pass


@ppt.command()
@click.argument("jugador")
@click.argument("cpu")
def jugar(jugador, cpu):
    jugador = jugador.lower()
    cpu = cpu.lower()

    if jugador not in OPCIONES or cpu not in OPCIONES:
        click.echo("❌ Jugada inválida")
        return

    if jugador == cpu:
        click.echo("🤝 Empate")
    elif (
        (jugador == "piedra" and cpu == "tijeras")
        or (jugador == "papel" and cpu == "piedra")
        or (jugador == "tijeras" and cpu == "papel")
    ):
        click.echo("✅ Ganaste")
    else:
        click.echo("❌ Perdiste")
