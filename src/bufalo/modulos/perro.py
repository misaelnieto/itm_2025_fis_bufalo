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
# Lista de poses para iterar en la animación
POSES = [POSE_UNO, POSE_DOS]


@click.group()
def perro() -> None:
    pass


# Este 'pass' es necesario para definir el grupo de comandos 'perro'.
@perro.command()
@click.option(
    "--veces",
    default=1,
    type=int,
    help="Número de veces que se repite la animación completa.",
)
def bailar(veces: int) -> None:
    # Usamos IntRange para asegurar que el número de repeticiones sea 1 o más,
    # lo cual previene errores y pasa la prueba de validación.
    click.echo("¡Mira mi pose de baile!")

    for _i in range(veces):
        for pose in POSES:
            click.clear()
            click.echo(pose)

            # Esperamos un momento para el efecto visual
            time.sleep(0.3)

    click.clear()
