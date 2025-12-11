import unittest
from buses import buses, Race

class TestBuses(unittest.TestCase):
    def test_buses_initial_positions(self):
        result = buses(0, 0, 0)
        lines = result.split('\n')
        self.assertEqual(len(lines), 15)  # 5 líneas por autobús + separadores
        self.assertTrue(lines[0].startswith('-' * 115))
        self.assertIn('RED BULL', lines[2])
        self.assertIn('MONSTER', lines[7])
        self.assertIn('Coca Cola', lines[12])

    def test_buses_with_positions(self):
        result = buses(10, 20, 30)
        lines = result.split('\n')
        # Verificar que las posiciones se reflejen en el espaciado
        self.assertIn('RED BULL', lines[3])
        self.assertIn('MONSTER', lines[8])
        self.assertIn('Coca Cola', lines[13])

class TestRace(unittest.TestCase):
    def test_race_initialization(self):
        race = Race()
        self.assertEqual(race.positions, [0, 0, 0])
        self.assertIsNone(race.winner)

    def test_advance_bus(self):
        race = Race()
        race.advance_bus(0)  # Advance RED BULL
        self.assertEqual(race.positions[0], 1)
        race.advance_bus(1)  # Advance MONSTER
        self.assertEqual(race.positions[1], 1)
        race.advance_bus(2)  # Advance Coca Cola
        self.assertEqual(race.positions[2], 1)

    def test_is_finished(self):
        race = Race()
        self.assertFalse(race.is_finished())
        race.positions[0] = 97
        self.assertTrue(race.is_finished())

    def test_get_winner(self):
        race = Race()
        race.positions[0] = 97
        self.assertEqual(race.get_winner(), "RED BULL")
        race.positions[0] = 0
        race.positions[1] = 97
        self.assertEqual(race.get_winner(), "MONSTER")
        race.positions[1] = 0
        race.positions[2] = 97
        self.assertEqual(race.get_winner(), "Coca Cola")

if __name__ == '__main__':
    unittest.main()
