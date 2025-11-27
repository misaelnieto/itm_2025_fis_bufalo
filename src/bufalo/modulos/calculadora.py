import click


@click.group()
def calculadora() -> None:
    """Comandos de la calculadora."""
    pass


@calculadora.command()
@click.argument("nums", nargs=-1, type=float)
def suma(nums: tuple[float, ...]) -> None:
    """Suma n números."""
    result = sum(nums)
    click.echo(f"Resultado: {result}")


@calculadora.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def resta(a: float, b: float) -> None:
    """Resta dos números."""
    result = a - b
    click.echo(f"Resultado: {result}")


@calculadora.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def multiplica(a: float, b: float) -> None:
    """Multiplica dos números."""
    result = a * b
    click.echo(f"Resultado: {result}")


@calculadora.command()
@click.argument("a", type=float)
@click.argument("b", type=float)
def divide(a: float, b: float) -> None:
    """Divide dos números."""
    if b == 0:
        click.echo("Error: No se puede dividir por cero.")
        return
    result = a / b
    click.echo(f"Resultado: {result}")
