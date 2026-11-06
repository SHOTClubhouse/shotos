import unittest

from inventory import reorder_level


class ReorderTests(unittest.TestCase):
    def test_whole_numbers(self):
        self.assertEqual(reorder_level(10, 3), 50)

    def test_rounds_up(self):
        self.assertEqual(reorder_level(2.5, 3, safety_days=1), 10)


if __name__ == "__main__":
    unittest.main()
