import importlib
import pkgutil

import click
# 🚨 IMPORTACIÓN REQUERIDA: Necesitamos la clase AnimalRace
from bufalo.modulos.animal_race import AnimalRace

import bufalo.modulos


@click.group()
def main() -> None:
    """
    🦬  Bufalo 🦬
    """
    pass


def autodiscover() -> None:
    """
    Descubre y registra automáticamente comandos desde el paquete bufalo.modulos.
    Busca objetos click.Group en cada módulo y los agrega al CLI principal.
    """
    path = bufalo.modulos.__path__
    prefix = bufalo.modulos.__name__ + "."

    for _, name, _ in pkgutil.iter_modules(path, prefix):
        try:
            module = importlib.import_module(name)
            for item_name in dir(module):
                item = getattr(module, item_name)
                
                if isinstance(item, click.Group):
                    item_module = getattr(item, "__module__", "")
                    
                    if item_module == "click.core":
                        callback = getattr(item, "callback", None)
                        if callback:
                            item_module = getattr(callback, "__module__", "")

                    if item_module == module.__name__:
                        main.add_command(item)
        except Exception as e:
            click.echo(f"Error cargando módulo {name}: {e}", err=True) # pragma: no cover



@main.group(name='animal_race') # Registra el grupo 'animal_race' bajo 'main'
def animal_race_cli() -> None:
    """Comandos para iniciar la simulación de carrera de animales."""
    pass

@animal_race_cli.command(name='run') # Define la acción 'run' bajo 'animal_race'
@click.option('-n', '--num', type=int, default=3, 
              help='Número de competidores.', show_default=True)
@click.option('-w', '--win', type=int, default=15, 
              help='Posición final requerida para ganar.', show_default=True)
def run_race(num: int, win: int) -> None:
    """
    Inicia la simulación de la carrera.
    Uso: uv run bufalo animal_race run
    """
    
    click.echo(f"🏁 Iniciando simulación de carrera (Ganador en posición: {win}) 🏁")
    try:
        race = AnimalRace(num_competitors=num, winning_position=win)
        race.run_simulation() 
    except Exception as e:
        click.echo(f"Error al ejecutar la simulación: {e}", err=True) # pragma: no cover
        

# 🚨 FIN DE LA SECCIÓN AGREGADA 🚨


autodiscover() # Mantenemos la autodetección original, que seguirá funcionando para otros módulos.


# Ahora, registramos el comando 'animal_race_cli' si no se detectó ya
# (Aunque en este caso, lo hemos definido manualmente, así que la llamada no es crítica aquí).
# main.add_command(animal_race_cli) # Ya está registrado por el decorador @main.group


if __name__ == "__main__": # pragma: no cover
    main()