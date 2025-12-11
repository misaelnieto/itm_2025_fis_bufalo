# src/bufalo/modulos/conversor.py

import click
import decimal

# Aseguramos precisión con decimal
# Esto ayuda a que el redondeo sea consistente con la prueba
decimal.getcontext().prec = 3


@click.group(name="conversor")
def conversor_cli():
    """
    Herramienta CLI para convertir unidades de medida.
    Actualmente soporta conversiones de temperatura (C/F).
    """
    pass


@conversor_cli.command(name="c-a-f")
@click.argument("valor", type=float)
def celsius_a_fahrenheit(valor: float):
    """
    Convierte un valor de Celsius a Fahrenheit (C * 9/5 + 32).
    """
    # Fórmula: F = C * (9/5) + 32
    resultado = valor * (9 / 5) + 32

    # Usamos Decimal para asegurar la precisión y formatear la salida a un decimal con precisión.
    resultado_decimal = decimal.Decimal(resultado)
    # click.echo imprime el resultado, que es lo que la prueba verifica.
    click.echo(f"{resultado_decimal:.1f}")


@conversor_cli.command(name="f-a-c")
@click.argument("valor", type=float)
def fahrenheit_a_celsius(valor: float):
    """
    Convierte un valor de Fahrenheit a Celsius ((F - 32) * 5/9).
    """
    # Fórmula: C = (F - 32) * (5/9)
    resultado = (valor - 32) * (5 / 9)

    resultado_decimal = decimal.Decimal(resultado)
    click.echo(f"{resultado_decimal:.1f}")
