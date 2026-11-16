import itertools
import re
import unittest
from pathlib import Path

OUTPUT = Path(__file__).resolve().parents[1] / "examples" / "show-me" / "output.md"
BANDS = ("Under 12", "12 to 15", "Over 15")


class ShowMeExample(unittest.TestCase):
    def setUp(self):
        self.text = OUTPUT.read_text(encoding="utf-8")
        self.fees = {}
        for band in BANDS:
            row = re.search(rf"^\| {band} \| \d+ \| (\d+) \| (\d+) \|", self.text, re.M)
            self.fees[band] = (int(row[1]), int(row[2]))

    def cost(self, counts, column):
        return sum(n * self.fees[band][column] for band, n in zip(BANDS, counts))

    def test_every_family_shape_the_proof_line_covers_is_stated_correctly(self):
        proof = next(line for line in self.text.splitlines() if line.startswith("- **What it proves:**"))
        # The line must not draw a conclusion from one band alone: the bands offset each other.
        self.assertNotIn("holds for families with a child under 12", proof)
        under, middle, over = (self.fees[band][0] - self.fees[band][1] for band in BANDS)
        self.assertIn(f"{-over} pounds for each child over 15", proof)
        self.assertIn(f"{under} pounds for each child under 12", proof)
        self.assertIn(f"{middle} pounds for each child aged 12 to 15", proof)
        # The rule in the line agrees with the fees for every family of up to six children.
        for counts in itertools.product(range(7), repeat=3):
            if 0 < sum(counts) <= 6:
                more = self.cost(counts, 1) > self.cost(counts, 0)
                self.assertEqual(more, -over * counts[2] > under * counts[0] + middle * counts[1], counts)

    def test_the_counter_example_is_shown_with_its_totals(self):
        counts = (1, 0, 3)
        self.assertEqual((self.cost(counts, 0), self.cost(counts, 1)), (240, 250))
        self.assertIn("one child under 12 and three over 15 pays 250 pounds instead of 240", self.text)


if __name__ == "__main__":
    unittest.main()
