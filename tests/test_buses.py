import pytest
from buses import buses, Race

def test_buses_output():
    # Test buses function with initial positions
    result = buses(0, 0, 0)
    lines = result.split('\n')
    assert len(lines) == 15  # 5 lines per bus + separators
    assert 'RED BULL' in result
    assert 'MONSTER' in result
    assert 'Coca Cola' in result

def test_buses_positions():
    # Test with different positions
    result = buses(10, 20, 30)
    assert 'RED BULL' in result
    assert 'MONSTER' in result
    assert 'Coca Cola' in result

def test_race_initialization():
    race = Race()
    assert race.positions == [0, 0, 0]
    assert race.winner is None

def test_advance_bus():
    race = Race()
    race.advance_bus(0)  # Advance RED BULL
    assert race.positions == [1, 0, 0]
    race.advance_bus(1)  # Advance MONSTER
    assert race.positions == [1, 1, 0]

def test_advance_bus_invalid_index():
    race = Race()
    race.advance_bus(3)  # Invalid index
    assert race.positions == [0, 0, 0]  # Should not change

def test_is_finished():
    race = Race()
    assert not race.is_finished()
    race.positions[0] = 97
    assert race.is_finished()

def test_get_winner():
    race = Race()
    assert race.get_winner() is None
    race.positions[0] = 97
    race.advance_bus(0)  # This should set winner
    assert race.get_winner() == "RED BULL"

def test_race_simulation():
    race = Race()
    while not race.is_finished():
        bus = 0  # Always advance first bus for test
        race.advance_bus(bus)
    assert race.get_winner() == "RED BULL"
