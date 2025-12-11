import click


@click.group()
def temperatura():
    """Convierte temperaturas entre grados Celsius y Fahrenheit."""
    pass


@temperatura.command()
@click.argument("celsius", type=float)
def acelsius(celsius):
    """Convierte grados Celsius a Fahrenheit."""
    f = (celsius * 9 / 5) + 32
    click.echo(f)


@temperatura.command()
@click.argument("fahrenheit", type=float)
def afahrenheit(fahrenheit):
    """Convierte Fahrenheit a Celsius."""
    c = (fahrenheit - 32) * 5 / 9
    click.echo(c)
