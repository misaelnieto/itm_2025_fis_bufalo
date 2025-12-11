import random

import click


def generar_historia():
    personajes = ["un dragón", "una princesa", "un robot", "un explorador"]
    lugares = ["en un castillo", "en la luna", "en un bosque", "en una cueva"]
    problemas = [
        "perdió su ruta",
        "encontró un misterio",
        "buscaba un tesoro",
        "tenía un gran desafío",
    ]

    return (
        f"Había una vez {random.choice(personajes)} "
        f"que vivía {random.choice(lugares)} "
        f"y {random.choice(problemas)}."
    )


# Define el grupo principal del comando
@click.group()
def historias():
    """Comandos para generar historias aleatorias."""
    pass


# Define el subcomando 'generar'
@historias.command()
def generar():
    """Genera e imprime una historia aleatoria."""
    click.echo(generar_historia())
