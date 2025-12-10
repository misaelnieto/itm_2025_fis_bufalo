import click
import json
import os

ESTADO_ARCHIVO = "cajero_estado.json"


def cargar_estado():
    if os.path.exists(ESTADO_ARCHIVO):
        try:
            with open(ESTADO_ARCHIVO, "r") as f:
                estado = json.load(f)
                return estado.get("saldo", 1000.0), estado.get("movimientos", [])
        except:
            return 1000.0, []
    return 1000.0, []


def guardar_estado(saldo, movimientos):
    estado = {"saldo": saldo, "movimientos": movimientos}
    with open(ESTADO_ARCHIVO, "w") as f:
        json.dump(estado, f)


saldo, movimientos = cargar_estado()
pin = "1234"


@click.group()
def cajero() -> None:
    """Cajero automático - PIN default: 1234"""
    pass


@cajero.command()
@click.option("--pin-input", prompt="PIN", hide_input=True)
def consultar(pin_input: str) -> None:
    global saldo
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    click.echo(f"Saldo: ${saldo}")


@cajero.command()
@click.option("--pin-input", prompt="PIN", hide_input=True)
@click.argument("monto", type=float)
def depositar(pin_input: str, monto: float) -> None:
    global saldo, movimientos
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    if monto <= 0:
        click.echo("Monto debe ser positivo")
        return
    saldo += monto
    movimientos.append(f"Depósito: +${monto}")
    guardar_estado(saldo, movimientos)
    click.echo(f"Depositado: ${monto}")
    click.echo(f"Nuevo saldo: ${saldo}")


@cajero.command()
@click.option("--pin-input", prompt="PIN", hide_input=True)
@click.argument("monto", type=float)
def retirar(pin_input: str, monto: float) -> None:
    global saldo, movimientos
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    if monto <= 0:
        click.echo("Monto debe ser positivo")
        return
    if monto > saldo:
        click.echo("Fondos insuficientes")
        return
    saldo -= monto
    movimientos.append(f"Retiro: -${monto}")
    guardar_estado(saldo, movimientos)
    click.echo(f"Retirado: ${monto}")
    click.echo(f"Nuevo saldo: ${saldo}")


@cajero.command()
@click.option("--pin-input", prompt="PIN", hide_input=True)
def tipo_cambio(pin_input: str) -> None:
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return

    click.echo("Tipo de cambio actual:")
    click.echo("  USD -> MXN: $18.50")
    click.echo("  EUR -> MXN: $20.10")
    click.echo("  GBP -> MXN: $23.75")
    click.echo("Ultima actualizacion: Hoy")


if __name__ == "__main__":
    cajero()
