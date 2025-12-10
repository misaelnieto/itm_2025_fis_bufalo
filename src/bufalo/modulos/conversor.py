from __future__ import annotations

from typing import Dict, Final

import click

UNIDADES: Final[Dict[str, float]] = {
    "km": 1000.0,
    "m": 1.0,
    "cm": 0.01,
}


@click.group()
def conversor() -> None:
    """Comandos de conversión de unidades básicas."""
    return


@conversor.command()
@click.argument("valor", type=float)
@click.argument("de", type=str)
@click.argument("a", type=str)
def convertir(valor: float, de: str, a: str) -> None:
    """Convierte VALOR desde la unidad DE hacia la unidad A."""
    unidad_origen = de.lower()
    unidad_destino = a.lower()

    if unidad_origen not in UNIDADES or unidad_destino not in UNIDADES:
        unidades_disponibles = ", ".join(UNIDADES.keys())
        mensaje = f"Error: Unidad no válida. Usa únicamente: {unidades_disponibles}"
        raise click.ClickException(mensaje)

    en_metros = valor * UNIDADES[unidad_origen]
    resultado = en_metros / UNIDADES[unidad_destino]

    click.echo(f"Resultado: {resultado}")
