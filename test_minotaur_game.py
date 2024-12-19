import unittest
from unittest.mock import patch

from Minotaur_game import (
    initialize_game, move_player, check_boundaries,
    check_barriers, throw_spear, minotaur_charge, trapdoor
)

class TestMinotaurGame(unittest.TestCase):
    def setUp(self):
        # Set random seed for reproducible tests
        self.player = {
            'level': 2,
            'x': 0,
            'y': 0,
            'spear': True
        }
        self.minotaur = {
            'level': 2,
            'x': 5,
            'y': 5
        }
        self.barriers = [(1, 1), (-2, -2), (3, 3)]

    def test_initialize_game(self):
        player, minotaur, barriers = initialize_game()
        # Check structure and value ranges
        self.assertIn('level', player)
        self.assertIn('x', player)
        self.assertIn('y', player)
        self.assertIn('spear', player)
        self.assertTrue(1 <= player['level'] <= 3)
        self.assertTrue(-10 <= player['x'] <= 10)
        self.assertTrue(-10 <= player['y'] <= 10)
        self.assertTrue(player['spear'])
        self.assertEqual(len(barriers), 10)

    def test_move_player(self):
        # Test each movement direction
        expected_positions = [
            (1, 1, 0),  # East
            (2, -1, 0), # West
            (3, 0, 1),  # North
            (4, 0, -1), # South
            (5, 0, 0),  # Up
            (6, 0, 0)   # Down
        ]
        for direction, expected_x_change, expected_y_change in expected_positions:
            player = {'x': 0, 'y': 0, 'level': 2}
            original_x = player['x']
            original_y = player['y']
            original_level = player['level']
            move_player(player, direction)
            if direction <= 4:
                self.assertEqual(player['x'], original_x + expected_x_change)
                self.assertEqual(player['y'], original_y + expected_y_change)
                self.assertEqual(player['level'], original_level)
            else:
                self.assertEqual(player['x'], original_x)
                self.assertEqual(player['y'], original_y)
                self.assertEqual(player['level'], original_level + (1 if direction == 5 else -1))
    
    def test_check_boundaries(self):
        test_cases = [
            ({'x': 11, 'y': 0, 'level': 2}, True),
            ({'x': -11, 'y': 0, 'level': 2}, True),
            ({'x': 0, 'y': 11, 'level': 2}, True),
            ({'x': 0, 'y': -11, 'level': 2}, True),
            ({'x': 0, 'y': 0, 'level': 0}, True),
            ({'x': 0, 'y': 0, 'level': 4}, True),
            ({'x': 10, 'y': 10, 'level': 1}, False),
        ]
        for player, expected in test_cases:
            self.assertEqual(check_boundaries(player), expected)

    def test_check_barriers(self):
        barriers = [(1, 1), (-2, -2)]
        test_cases = [
            ({'x': 1, 'y': 1}, True),
            ({'x': -2, 'y': -2}, True),
            ({'x': 0, 'y': 0}, False),
            ({'x': 1, 'y': 0}, False),
        ]
        for player, expected in test_cases:
            self.assertEqual(check_barriers(player, barriers), expected)

    def test_throw_spear(self):
        test_cases = [
            # Different levels
            ({'level': 1, 'x': 0, 'y': 0}, {'level': 2, 'x': 0, 'y': 0}, False),
            # Same level, aligned on x, within range
            ({'level': 2, 'x': 0, 'y': 0}, {'level': 2, 'x': 0, 'y': 5}, True),
            # Same level, aligned on y, within range
            ({'level': 2, 'x': 0, 'y': 0}, {'level': 2, 'x': 5, 'y': 0}, True),
            # Same level, not aligned, within range
            ({'level': 2, 'x': 0, 'y': 0}, {'level': 2, 'x': 5, 'y': 5}, False),
            # Too far away
            ({'level': 2, 'x': 0, 'y': 0}, {'level': 2, 'x': 15, 'y': 0}, False),
        ]
        for player, minotaur, expected in test_cases:
            player['spear'] = True
            result = throw_spear(player, minotaur)
            self.assertEqual(result, expected)

    @patch('random.random')
    def test_minotaur_charge(self, mock_random):
        mock_random.return_value = 0.2  # Will trigger charge
        test_cases = [
            # Format: player pos, minotaur pos, expected result
            ({'x': 0, 'y': 0, 'level': 2}, {'x': 1, 'y': 1, 'level': 2}, True),
            ({'x': 0, 'y': 0, 'level': 2}, {'x': 5, 'y': 5, 'level': 2}, False),
            ({'x': 0, 'y': 0, 'level': 1}, {'x': 1, 'y': 1, 'level': 2}, False)
        ]
        for player, minotaur, expected in test_cases:
            result = minotaur_charge(minotaur, player)
            self.assertEqual(result, expected,
                f"Failed for player at ({player['x']},{player['y']}) level {player['level']}, "
                f"minotaur at ({minotaur['x']},{minotaur['y']}) level {minotaur['level']}")

    @patch('random.random')
    def test_trapdoor(self, mock_random):
        mock_random.return_value = 0.05  # Will trigger trapdoor
        test_cases = [
            ({'level': 1}, True),  # Falls out of cavern
            ({'level': 2}, False), # Falls but survives
            ({'level': 3}, False), # Falls but survives
        ]
        for player, expected in test_cases:
            result = trapdoor(player)
            self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()