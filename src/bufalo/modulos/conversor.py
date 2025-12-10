from __future__ import annotations

from typing import Dict, Final

import click

UNIDADES: Final[Dict[str, float]] = {
    "m": 1.0,
    "cm": 0.01,
    "km": 1000.0,
}


@click.group(
    help=(
        "Herramientas para convertir unidades de longitud.\n\n"
        "Ejemplos:\n"
        "  bufalo conversor convertir 20 m cm   -> 2000.0\n"
        "  bufalo conversor convertir 5 km m    -> 5000.0\n"
    )
)
def conversor() -> None:
    """Grupo de comandos para conversión de unidades."""
    pass


@conversor.command(
    help=(
        "Convierte un VALOR de una unidad a otra.\n\n"
        "Uso:\n"
        "  bufalo conversor convertir VALOR DE A\n\n"
        "Parámetros:\n"
        "  VALOR  Número a convertir (ej. 20)\n"
        "  DE     Unidad origen  (m, cm, km)\n"
        "  A      Unidad destino (m, cm, km)\n\n"
        "Ejemplo:\n"
        "  bufalo conversor convertir 20 km m   -> 20000.0\n"
    )
)
@click.argument("valor", type=float)
@click.argument("de", metavar="DE")
@click.argument("a", metavar="A")
def convertir(valor: float, de: str, a: str) -> None:
    """Convierte VALOR de la unidad DE a la unidad A."""
    if de not in UNIDADES or a not in UNIDADES:
        # Click antepone "Error: " al mensaje
        raise click.ClickException("Unidad no válida. Unidades soportadas: km, m, cm")

    valor_en_metros = valor * UNIDADES[de]
    resultado = valor_en_metros / UNIDADES[a]

    click.echo(f"Resultado: {resultado}")
