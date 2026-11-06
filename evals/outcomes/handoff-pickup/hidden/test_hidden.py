"""Hidden checks for the handoff pickup: what Sam's note promised, run against the result."""
import unittest
from pathlib import Path

import inventory


def names(result):
    """Item names from whatever shape the report returns: names, (name, ...) tuples, dicts or a mapping."""
    if isinstance(result, dict):
        return list(result)
    out = []
    for item in result:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            out.append(item.get("item") or item.get("name"))
        else:
            out.append(item[0])
    return out


class Hidden(unittest.TestCase):
    def test_reorder_level_is_correct(self):
        # Sam's note says safety stock is in days of usage: 10 a day for 3 days plus 2 safety days = 50.
        self.assertEqual(inventory.reorder_level(10, 3), 50)
        self.assertEqual(inventory.reorder_level(2.5, 3, safety_days=1), 10)

    def test_load_stock(self):
        stock = inventory.load_stock(str(Path(__file__).parent / "stock.csv"))
        self.assertEqual(stock["yeast"], 8)
        self.assertEqual(len(stock), 5)

    def test_low_stock_report(self):
        stock = {"butter": 40, "caster sugar": 120, "eggs": 90, "strong flour": 300, "yeast": 8}
        usage = {"butter": 12, "caster sugar": 20, "eggs": 45, "strong flour": 60, "yeast": 3}
        lead = {"butter": 2, "caster sugar": 4, "eggs": 1, "strong flour": 3, "yeast": 2}
        # reorder levels with 2 safety days: butter 48, sugar 120, eggs 135, flour 300, yeast 12
        self.assertEqual(names(inventory.low_stock_report(stock, usage, lead)),
                         ["butter", "caster sugar", "eggs", "strong flour", "yeast"])

    def test_low_stock_report_excludes_items_above_level(self):
        stock = {"butter": 100, "yeast": 8}
        usage = {"butter": 12, "yeast": 3}
        lead = {"butter": 2, "yeast": 2}
        self.assertEqual(names(inventory.low_stock_report(stock, usage, lead)), ["yeast"])


if __name__ == "__main__":
    unittest.main()
