import re
from collections import Counter

import click


def _limpiar_y_dividir(texto: str) -> list[str]:
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9]+", " ", texto)
    return [p for p in texto.split() if p]


@click.group()
def palabras() -> None:
    """Comandos para trabajar con palabras de un texto."""
    pass


@palabras.command()
@click.argument("texto", type=str)
def contar(texto: str) -> None:
    """Cuenta el número total de palabras en un TEXTO."""
    palabras = _limpiar_y_dividir(texto)
    click.echo(len(palabras))


@palabras.command()
@click.argument("texto", type=str)
@click.option(
    "-n",
    "--top",
    type=int,
    default=5,
    show_default=True,
    help="Número de palabras más frecuentes a mostrar.",
)
def top(texto: str, top: int) -> None:
    """Muestra las N palabras más frecuentes de un TEXTO."""
    palabras = _limpiar_y_dividir(texto)
    contador = Counter(palabras)
    for palabra, cantidad in contador.most_common(top):
        click.echo(f"{palabra}: {cantidad}")
