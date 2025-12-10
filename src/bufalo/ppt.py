import random

import click


@click.group()
def ppt():
    """Juego de Piedra, Papel o Tijera"""
    pass


@ppt.command()
@click.argument("jugada")
def jugar(jugada):
    opciones = ["piedra", "papel", "tijera"]
    jugada = jugada.lower()

    if jugada not in opciones:
        click.echo("Opción inválida")
        return

    cpu = random.choice(opciones)

    if jugada == cpu:
        resultado = "Empate"
    elif (
        (jugada == "piedra" and cpu == "tijera")
        or (jugada == "papel" and cpu == "piedra")
        or (jugada == "tijera" and cpu == "papel")
    ):
        resultado = "Ganaste"
    else:
        resultado = "Perdiste"

    click.echo(f"Tú: {jugada}")
    click.echo(f"CPU: {cpu}")
    click.echo(resultado)
