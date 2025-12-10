import random

import click

OPCIONES = ["piedra", "papel", "tijeras"]


@click.group(help="Juego de Piedra, Papel o Tijeras")
def ppt():
    pass


@ppt.command(help="Juega contra la CPU (la CPU elige random).")
@click.argument("jugador", type=click.Choice(OPCIONES))
def jugar(jugador):
    """Juega contra la CPU (esta se elige al azar)."""
    cpu = random.choice(OPCIONES)

    click.echo(f"👤 Tú: {jugador}")
    click.echo(f"🤖 CPU: {cpu}")

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
