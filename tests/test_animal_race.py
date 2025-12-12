# tests/test_animal_race.py

import pytest

# 🚨 Usamos la ruta corregida para la importación
from bufalo.modulos.animal_race import AnimalRace

WIN_POS = 10  # Posición simplificada para testeo


def test_race_initialization_and_default_state():
    """Cubre __init__ y el estado inicial."""
    race = AnimalRace(2, WIN_POS)
    assert race.positions == [0, 0]
    assert race.winner is None
    assert not race.is_finished()  # Cubre is_finished() -> False


def test_advance_animal_normal():
    """Cubre el avance normal y la rama 'if index' -> True."""
    race = AnimalRace(3, WIN_POS)
    race.advance_animal(1)
    assert race.positions == [0, 1, 0]


def test_advance_animal_invalid_index_coverage():
    """Cubre la rama 'if index' -> False (índice fuera de rango)."""
    race = AnimalRace(2, WIN_POS)
    race.positions = [5, 5]
    initial_positions = list(race.positions)

    # Índice inválido
    race.advance_animal(5)
    race.advance_animal(-1)

    assert race.positions == initial_positions  # Nada debe haber cambiado


def test_win_condition_coverage():
    """Cubre la rama 'if self.positions >= winning_position' -> True."""
    race = AnimalRace(1, 5)

    race.positions = [4]
    race.advance_animal(0)  # Gana en el paso 5

    assert race.positions == [5]
    assert race.is_finished()  # Cubre is_finished() -> True
    assert race.get_winner() == 0


def test_first_winner_only():
    """Asegura que solo el primer animal que gana es registrado (if self.winner is None)."""
    race = AnimalRace(2, 5)
    race.positions = [4, 4]

    race.advance_animal(0)  # Animal 0 gana (winner = 0)
    race.advance_animal(1)  # Animal 1 también cruza, pero es ignorado

    assert race.positions == [5, 5]
    assert race.get_winner() == 0  # El ganador debe ser el primero (Animal 0)


def test_run_simulation_coverage_exclusion():
    """
    Solo para asegurar que la función run_simulation exista, asumiendo que
    la exclusión # pragma: no cover está dentro.
    """
    race = AnimalRace(1, 1)
    race.run_simulation()
    # Esta prueba no comprueba lógica, solo asegura que la llamada existe
    pass
