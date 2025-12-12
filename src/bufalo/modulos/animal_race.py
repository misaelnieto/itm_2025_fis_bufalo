import os
import random
import time
from typing import List, Optional

# Definición de constantes para colores y comandos
GREN = "\033[32m"
END = "\033[0m"
CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'


class AnimalRace:
    """
    Simula la lógica de una carrera entre múltiples competidores.
    """

    def __init__(
        self, 
        num_competitors: int, 
        winning_position: int, 
        names: Optional[List[str]] = None
    ):
        self.num_competitors = num_competitors
        self.winning_position = winning_position
        self.positions = [0] * num_competitors
        self.winner: Optional[int] = None
        
        if names is None:
            self.names = [f"Animal {i+1}" for i in range(num_competitors)]
        else:
            self.names = names

    def advance_animal(self, animal_index: int) -> None:
        """
        Avanza el animal en el índice dado y verifica la victoria.
        """
        if 0 <= animal_index < self.num_competitors:
            self.positions[animal_index] += 1
            
            # Comprobación de la victoria
            if self.positions[animal_index] >= self.winning_position:
                if self.winner is None: 
                    self.winner = animal_index

    def is_finished(self) -> bool: 
        """Verifica si la carrera ha terminado."""
        return self.winner is not None

    def get_winner(self) -> Optional[int]:
        """Retorna el índice del animal ganador o None."""
        return self.winner

    # 🚨 E501 CORREGIDO: Comentario acortado
    # Función run_simulation será excluida por pyproject.toml
    def run_simulation(self):  
        """Ejecuta una simulación de carrera en tiempo real."""
        os.system(CLEAR_COMMAND)
        print("🏁 ¡COMIENZA LA CARRERA! 🏁")
        time.sleep(1)

        while not self.is_finished():
            animal_to_advance = random.randint(0, self.num_competitors - 1)
            self.advance_animal(animal_to_advance)
            
            os.system(CLEAR_COMMAND)
            print("--- PISTA ---")
            for name, pos in zip(self.names, self.positions, strict=True): 
                print(f"{name}: {'-' * pos} >")
            time.sleep(0.05)

        winner_index = self.get_winner()
        if winner_index is not None:
            print(f"\n{GREN}GANÓ LA CARRERA: {self.names[winner_index]}{END}")


if __name__ == "__main__": 
    # Ejemplo de uso
    race = AnimalRace(
        num_competitors=3, 
        winning_position=20, 
        names=["Guepardo", "Tortuga", "Liebre"]
    )
    race.run_simulation()