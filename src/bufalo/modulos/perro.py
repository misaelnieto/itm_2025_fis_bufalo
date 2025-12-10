import time

import click

POSE_UNO = """
  (\\_/)
 ( o.o )  
 > ^ < 
  /   \\
  U---U
"""

POSE_DOS = """
  (\\_/)
 ( ^.^ )  
 >  ^  < 
  /   |
  U---U
"""
# Almacenamos las poses en una lista para iterar
POSES = [POSE_UNO, POSE_DOS]


@click.group()  # <--- ¡Esto define la función 'perro' que se debe exportar!
def perro() -> None:
    """Comandos para mostrar un perro bailando en ASCII."""
    pass


@perro.command()
@click.option(
    "--veces",
    default=1,
    type=int,
    help="Número de veces que se repite la animación completa.",
)
def bailar(veces: int) -> None:
    """Muestra una animación simple de un perro bailando."""

    click.echo("¡Mira mi pose de baile!")

    for i in range(veces):
        for pose in POSES:
            # Imprimimos la pose, limpiando la pantalla para el efecto de animación
            click.clear()
            click.echo(pose)

            # Esperamos un momento para el efecto visual
            time.sleep(0.3)

    click.clear()
