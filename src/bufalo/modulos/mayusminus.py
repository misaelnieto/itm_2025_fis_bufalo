import click


@click.group()
def mayusminus() -> None:
    """Conversor de mayúsculas, minúsculas y ASCII."""
    pass


@mayusminus.command()
@click.argument("texto", type=str)
# Se introducirá un string y se devolverá el string en mayúsculas
def mayuscula(texto: str) -> None:
    """Convierte el texto a mayúsculas."""
    result = texto.upper()
    click.echo(result)


@mayusminus.command()
@click.argument("texto", type=str)
# Se introducirá un string y se devolverá el string en minúsculas
def minuscula(texto: str) -> None:
    """Convierte el texto a minúsculas."""
    result = texto.lower()
    click.echo(result)


@mayusminus.command(name="toascii")
@click.argument("texto", type=str)
# El sep sirve como separador entre los códigos ASCII para cada caracter
# en el texto
@click.option("--sep", default=" ", help="Separador entre códigos ASCII")
def toascii(texto: str, sep: str) -> None:
    """Convierte cada carácter del texto a su código ASCII separado por 'sep'"""
    codes = [str(ord(c)) for c in texto]
    click.echo(sep.join(codes))


@mayusminus.command(name="fromascii")
@click.argument("texto", type=str)
@click.option("--sep", default=" ", help="Separador usado entre códigos ASCII")
def fromascii(texto: str, sep: str) -> None:
    """Convierte códigos ASCII separados por sep a texto."""
    parts = [p for p in texto.split(sep) if p != ""]
    try:
        chars = [chr(int(s)) for s in parts]
    except ValueError:
        click.echo(
            "Entrada inválida: "
            "asegúrate de proporcionar números ASCII separados correctamente.",
            err=True,
        )
        raise click.Abort() from None
    click.echo("".join(chars))
