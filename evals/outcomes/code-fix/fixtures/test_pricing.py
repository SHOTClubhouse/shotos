import unittest

from pricing import apply_discount, basket_total, line_total


class PricingTests(unittest.TestCase):
    def test_line_total(self):
        self.assertEqual(line_total(250, 4), 1000)

    def test_save10(self):
        self.assertEqual(apply_discount(2000, "SAVE10"), 1800)

    def test_fiver_applies_at_exactly_the_threshold(self):
        self.assertEqual(apply_discount(2500, "FIVER"), 2000)

    def test_fiver_does_not_apply_below_threshold(self):
        self.assertEqual(apply_discount(2499, "FIVER"), 2499)

    def test_unknown_code_changes_nothing(self):
        self.assertEqual(apply_discount(1234, "NOPE"), 1234)

    def test_basket_total_includes_vat(self):
        self.assertEqual(basket_total([(1000, 2)]), 2400)

    def test_basket_total_with_discount(self):
        self.assertEqual(basket_total([(1000, 3)], "FIVER"), 3000)


if __name__ == "__main__":
    unittest.main()
