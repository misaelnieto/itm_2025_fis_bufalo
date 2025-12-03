import click

# Datos iniciales del cajero
saldo = 1000.0
pin = "1234"

@click.group()
def cajero() -> None:
    """Comandos del cajero automático."""
    pass

@cajero.command()
@click.option("--pin-input", prompt="Ingresa tu PIN", hide_input=True)
def consultar(pin_input: str) -> None:
    """Consulta el saldo disponible."""
    global saldo
    
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    
    click.echo(f"Tu saldo es: ${saldo}")

@cajero.command()
@click.option("--pin-input", prompt="Ingresa tu PIN", hide_input=True)
@click.argument("monto", type=float)
def depositar(pin_input: str, monto: float) -> None:
    """Deposita dinero en la cuenta."""
    global saldo
    
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    
    if monto <= 0:
        click.echo("El monto debe ser mayor a 0")
        return
    
    saldo += monto
    click.echo(f"Depositado: ${monto}")
    click.echo(f"Nuevo saldo: ${saldo}")

@cajero.command()
@click.option("--pin-input", prompt="Ingresa tu PIN", hide_input=True)
@click.argument("monto", type=float)
def retirar(pin_input: str, monto: float) -> None:
    """Retira dinero de la cuenta."""
    global saldo
    
    if pin_input != pin:
        click.echo("PIN incorrecto")
        return
    
    if monto <= 0:
        click.echo("El monto debe ser mayor a 0")
        return
    
    if monto > saldo:
        click.echo("No tienes suficiente saldo")
        return
    
    saldo -= monto
    click.echo(f"Retirado: ${monto}")
    click.echo(f"Nuevo saldo: ${saldo}")

@cajero.command()
@click.option("--pin-actual", prompt="PIN actual", hide_input=True)
@click.option("--nuevo", prompt="Nuevo PIN", hide_input=True)
def cambiar_pin(pin_actual: str, nuevo: str) -> None:
    """Cambia el PIN de seguridad."""
    global pin
    
    if pin_actual != pin:
        click.echo("PIN actual incorrecto")
        return
    
    if len(nuevo) != 4:
        click.echo("El PIN debe tener 4 dígitos")
        return
    
    pin = nuevo
    click.echo("PIN cambiado correctamente")

if __name__ == "__main__":
    cajero()