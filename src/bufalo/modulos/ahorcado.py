import random

import click

# Dibujar el ahorcado con ascii
AHORCADO_ASCII = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
    """,
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
    """,
]


@click.group(invoke_without_command=True)
def ahorcado():
    """Juego del Ahorcado."""
    pass


@ahorcado.command()
@click.argument("palabra_secreta", required=False)
def jugar(palabra_secreta):
    """Inicia una partida del Ahorcado."""
    palabras = ["python", "programa", "computadora", "teclado", "raton"]
    palabra = random.choice(palabras)
    progreso = ["_"] * len(palabra)
    intentos = 6
    letras_usadas = []

    click.echo("=== Ahorcado ===")

    while intentos > 0:
        click.echo(AHORCADO_ASCII[6 - intentos])
        click.echo(f"\nPalabra: {' '.join(progreso)}")
        click.echo(f"Intentos restantes: {intentos}")
        click.echo(f"Letras usadas: {letras_usadas}")

        letra = input("Ingresa una letra: ").lower()

        if letra in letras_usadas:
            click.echo("Ya usaste esa letra")
            continue

        letras_usadas.append(letra)

        if letra in palabra:
            for i, ch in enumerate(palabra):
                if ch == letra:
                    progreso[i] = letra
        else:
            intentos -= 1

        if "_" not in progreso:
            click.echo(f"\n¡Ganaste! La palabra era: {palabra}")
            return

    click.echo(AHORCADO_ASCII[-1])
    click.echo(f"\nPerdiste... la palabra era: {palabra}")
