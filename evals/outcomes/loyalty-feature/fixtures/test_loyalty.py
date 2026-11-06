import unittest

from loyalty import points_for_order


class ExistingTests(unittest.TestCase):
    def test_ten_points_per_pound(self):
        self.assertEqual(points_for_order(1250), 120)

    def test_under_a_pound_earns_nothing(self):
        self.assertEqual(points_for_order(99), 0)


if __name__ == "__main__":
    unittest.main()
