# tests/test_animal_race.py

from bufalo.modulos.animal_race import AnimalRace

WIN_POS = 10 

def test_race_initialization_with_default_names():
    race = AnimalRace(2, WIN_POS, names=None)
    assert race.positions == [0, 0]
    assert race.names == ["Animal 1", "Animal 2"]
    assert not race.is_finished()

def test_race_initialization_with_custom_names():
    custom_names = ["Tortuga", "Liebre"]
    race = AnimalRace(2, WIN_POS, names=custom_names)
    assert race.names == custom_names

def test_advance_animal_normal():
    race = AnimalRace(3, WIN_POS)
    race.advance_animal(1)
    assert race.positions == [0, 1, 0]

def test_advance_animal_invalid_index_coverage():
    race = AnimalRace(2, WIN_POS)
    initial_positions = list(race.positions)
    race.advance_animal(5)
    race.advance_animal(-1)
    assert race.positions == initial_positions

def test_win_condition_and_winner_setter():
    race = AnimalRace(1, 5) 
    race.positions = [4]
    race.advance_animal(0) 
    assert race.positions == [5]
    assert race.is_finished()
    assert race.get_winner() == 0

def test_only_first_winner_is_registered():
    # 🚨 CORREGIDO E501: Docstring acortado
    """Asegura que solo el primer animal que gana es registrado."""
    race = AnimalRace(2, 5)
    race.positions = [4, 4]
    race.advance_animal(0) 
    race.advance_animal(1) 
    assert race.get_winner() == 0

def test_is_finished_logic():
    race = AnimalRace(1, 5)
    assert not race.is_finished()
    race.winner = 0 
    assert race.is_finished()

def test_get_winner_logic():
    race = AnimalRace(1, 5)
    assert race.get_winner() is None
    race.winner = 0
    assert race.get_winner() == 0

def test_run_simulation_coverage_exclusion():
    # 🚨 CORREGIDO E501: Docstring acortado
    """Asegura que run_simulation existe y es invocable."""
    race = AnimalRace(1, 1)
    race.run_simulation()
    pass