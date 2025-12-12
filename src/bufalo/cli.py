import importlib
import pkgutil

import click

import bufalo.modulos


@click.group()
def main() -> None:
    """
    🦬  Bufalo 🦬
    """
    pass


def autodiscover() -> None:
   
    path = bufalo.modulos.__path__
    prefix = bufalo.modulos.__name__ + "."

    for _, name, _ in pkgutil.iter_modules(path, prefix):
        try:
            module = importlib.import_module(name)
            for item_name in dir(module):
                item = getattr(module, item_name)
                
                
                if isinstance(item, (click.Group, click.Command)):
                    
                    
                    item_module = getattr(item, "__module__", "")
                    if item_module == "click.core":
                        callback = getattr(item, "callback", None)
                        if callback:
                            item_module = getattr(callback, "__module__", "")

                    if item_module == module.__name__ and item.name:
                        
                        if item.name != "main":
                            main.add_command(item)
                        
        except Exception as e:
            click.echo(f"Error cargando módulo {name}: {e}", err=True)



autodiscover()

if __name__ == "__main__":
    main()