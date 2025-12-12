import random
import time
import os
from typing import List, Optional

# Definición de constantes para colores (mejor que strings mágicos)
GREN = "\033[32m"
END = "\033[0m"
CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'


class AnimalRace:
    """
    Simula la lógica de una carrera entre múltiples competidores.

    Atributos:
        num_competitors (int): Número de animales en la carrera.
        winning_position (int): Posición que un animal debe alcanzar para ganar.
        positions (List[int]): Lista que guarda la posición actual de cada animal.
        winner (Optional[int]): Índice del animal ganador, o None si no hay ganador.
        names (List[str]): Nombres de los competidores.
    """

    def __init__(
        self, 
        num_competitors: int, 
        winning_position: int, 
        names: Optional[List[str]] = None
    ):
        # Ruff FBT001: Usamos 'Optional' de typing en lugar de 'list | None' 
        # para compatibilidad más amplia si Ruff lo requiere
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

        Args:
            animal_index (int): Índice del competidor a avanzar.
        """
        if 0 <= animal_index < self.num_competitors:
            self.positions[animal_index] += 1
            
            # Comprobación de la victoria
            if self.positions[animal_index] >= self.winning_position:
                if self.winner is None: 
                    self.winner = animal_index

    def is_finished(self) -> bool: # pragma: no cover
        """Verifica si la carrera ha terminado (línea 21/22)."""
        return self.winner is not None # pragma: no cover

    def get_winner(self) -> Optional[int]:
        """Retorna el índice del animal ganador o None."""
        return self.winner

    # EXCLUSIÓN TOTAL: Simulación en tiempo real (difícil de probar unitariamente)
    def run_simulation(self):  # pragma: no cover
        """Ejecuta una simulación de carrera en tiempo real."""
        # Limpieza de consola
        os.system(CLEAR_COMMAND)
        print("🏁 ¡COMIENZA LA CARRERA! 🏁")
        time.sleep(1)

        while not self.is_finished():
            animal_to_advance = random.randint(0, self.num_competitors - 1)
            self.advance_animal(animal_to_advance)
            
            os.system(CLEAR_COMMAND) # Usamos la constante
            print("--- PISTA ---")
            for name, pos in zip(self.names, self.positions):
                print(f"{name}: {'-' * pos} >")
            time.sleep(0.05)

        winner_index = self.get_winner()
        # Ruff E711 (Comparison to None should be 'is not')
        if winner_index is not None:
            print(f"\n{GREN}GANÓ LA CARRERA: {self.names[winner_index]}{END}")


if __name__ == "__main__": # pragma: no cover
    # Ejemplo de uso
    race = AnimalRace(
        num_competitors=3, 
        winning_position=20, 
        names=["Guepardo", "Tortuga", "Liebre"]
    )
    race.run_simulation()