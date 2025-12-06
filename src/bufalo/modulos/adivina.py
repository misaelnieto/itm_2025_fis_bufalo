import click
import random



@click.group()
def adivina():
    """Juego para adivinar un número."""
    pass


def evaluar_intento(objetivo: int, intento: int) -> str:
    if intento == objetivo:
        return "ganaste"
    elif intento < objetivo:
        return "muy bajo"
    else:
        return "muy alto"


# =====================================
#      JUEGO NORMAL (3 intentos)
# =====================================
@adivina.command()
def jugar():
    """Inicia el juego desde la línea de comandos (3 intentos)."""
    objetivo = random.randint(1, 100)
    click.echo("Adivina un número entre 1 y 100")
    click.echo("Tienes solo 3 intentos")

    for intento_num in range(1, 4):
        intento = click.prompt(f"Intento {intento_num}", type=int)
        resultado = evaluar_intento(objetivo, intento)
        click.echo(resultado)

        if resultado == "ganaste":
            return

    click.echo(f"Perdiste. El número era {objetivo}")


# =====================================
#      JUEGO DIFÍCIL (1 a 1000)
# =====================================
@adivina.command()
def dificil():
    """Modo difícil: número entre 1 y 1000 con 3 intentos."""
    objetivo = random.randint(1, 1000)
    click.echo("Modo difícil: adivina el número entre 1 y 1000")
    click.echo("Tienes solo 3 intentos")

    for intento_num in range(1, 4):
        intento = click.prompt(f"Intento {intento_num}", type=int)
        resultado = evaluar_intento(objetivo, intento)
        click.echo(resultado)

        if resultado == "ganaste":
            return

    click.echo(f"Perdiste. El número era {objetivo}")
