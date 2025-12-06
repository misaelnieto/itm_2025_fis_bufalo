import random

import click

RESULTADOS_VALIDOS = ("aguila", "sello")


def tirar_moneda():
    """Simula el lanzamiento de una moneda y devuelve 'aguila' o 'sello'."""
    return random.choice(RESULTADOS_VALIDOS)


def jugar_volado(apuesta, resultado_moneda):
    """
    Compara la apuesta del usuario con el resultado real de la moneda.
    Args:
        apuesta (str): La predicción del usuario.
        resultado_moneda (str): El resultado real de la tirada.
    Returns:
        bool: True si la apuesta coincide (gana).
    """
    apuesta = apuesta.lower()

    if apuesta not in RESULTADOS_VALIDOS or resultado_moneda not in RESULTADOS_VALIDOS:
        raise ValueError("Apuesta o resultado inválido. Debe ser 'aguila' o 'sello'.")

    return apuesta == resultado_moneda


# --- Función Principal como GRUPO (para Autodiscovery) ---


@click.group()
def volado():
    """
    Juega un volado. Usa 'bufalo volado lanzar <aguila|sello>'.
    """
    pass


# --- El Comando Real de Lanzamiento (Subcomando) ---


@volado.command()
@click.argument("apuesta", type=click.Choice(RESULTADOS_VALIDOS))
def lanzar(apuesta):
    """
    Lanza la moneda y verifica tu apuesta ('aguila' o 'sello').

    Ejemplo: bufalo volado lanzar aguila
    """
    # 1. Ejecutar lógica
    resultado_moneda = tirar_moneda()
    gana = jugar_volado(apuesta, resultado_moneda)

    # 2. Mostrar resultado (la interacción)
    click.echo(f" Apuesta: {apuesta.upper()}")
    click.echo(f" Resultado: {resultado_moneda.upper()} ")

    if gana:
        click.echo("\n¡Felicidades! ¡HAS GANADO EL VOLADO!")
    else:
        click.echo("\nLo siento. ¡HAS PERDIDO EL VOLADO! Vuelve a intentarlo.")
