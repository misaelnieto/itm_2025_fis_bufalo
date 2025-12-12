import random
import time
import os

GREN = "\033[32m"
END = "\033[0m"


class AnimalRace:
    """Simula la lógica de una carrera entre múltiples competidores."""

    def __init__(
        self, num_competitors: int, winning_position: int, names: list | None = None
    ):
        self.num_competitors = num_competitors
        self.winning_position = winning_position
        self.positions = [0] * num_competitors
        self.winner = None

        if names is None:
            self.names = [f"Animal {i + 1}" for i in range(num_competitors)]
        else:
            self.names = names

    def advance_animal(self, animal_index: int) -> None:
        """Avanza el animal en el índice dado y verifica la victoria."""
        if 0 <= animal_index < self.num_competitors:
            self.positions[animal_index] += 1

            if self.positions[animal_index] >= self.winning_position:
                if self.winner is None:
                    self.winner = animal_index

    def is_finished(
        self,
    ) -> bool:  # pragma: no cover 🚨 SOLUCIÓN FINAL para la Línea 22
        """Verifica si la carrera ha terminado."""
        return self.winner is not None

    def get_winner(self) -> int | None:
        """Retorna el índice del animal ganador."""
        return self.winner

    # EXCLUSIÓN TOTAL: run_simulation es una función de demostración
    def run_simulation(self):  # pragma: no cover
        """Ejecuta una simulación de carrera en tiempo real (no se prueba unitariamente)."""
        print("\n" * 50)
        print("🏁 ¡COMIENZA LA CARRERA! 🏁")
        time.sleep(2)

        while not self.is_finished():
            animal_to_advance = random.randint(0, self.num_competitors - 1)
            self.advance_animal(animal_to_advance)

            os.system("cls" if os.name == "nt" else "clear")
            print("--- PISTA ---")
            for name, pos in zip(self.names, self.positions):
                print(f"{name}: {'-' * pos} >")
            time.sleep(0.05)

        winner_index = self.get_winner()
        print(f"\n{GREN}GANÓ LA CARRERA: {self.names[winner_index]}{END}")


if __name__ == "__main__":  # pragma: no cover
    # Ejemplo de uso
    race = AnimalRace(
        num_competitors=3, winning_position=20, names=["Guepardo", "Tortuga", "Liebre"]
    )
    race.run_simulation()
