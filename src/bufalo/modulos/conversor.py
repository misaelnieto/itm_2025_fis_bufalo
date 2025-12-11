# src/bufalo/modulos/conversor.py

import click
# Nota: Se eliminó 'import decimal' y 'decimal.getcontext().prec = 3'
# para seguir la recomendación del bot de evitar cambios de estado global.


@click.group(name="conversor")
def conversor_cli():
    """
    Herramienta CLI para convertir unidades de medida.
    Actualmente soporta conversiones de temperatura (C/F).
    """
    pass


@conversor_cli.command(name="caf")
@click.argument("valor", type=float)
def celsius_a_fahrenheit(valor: float):
    """
    Convierte un valor de Celsius a Fahrenheit (C * 9/5 + 32).
    """
    # Fórmula: F = C * (9/5) + 32
    resultado = valor * (9 / 5) + 32 

    # Implementación corregida: Usar formato de float directamente para 1 decimal.
    click.echo(f"{resultado:.1f}")


@conversor_cli.command(name="fac")
@click.argument("valor", type=float)
def fahrenheit_a_celsius(valor: float):
    """
    Convierte un valor de Fahrenheit a Celsius ((F - 32) * 5/9).
    """
    # Fórmula: C = (F - 32) * (5/9)
    resultado = (valor - 32) * (5 / 9) 

    # Implementación corregida: Usar formato de float directamente para 1 decimal.
    click.echo(f"{resultado:.1f}")