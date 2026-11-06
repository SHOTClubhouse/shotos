"""Hidden acceptance tests: the unambiguous examples from TICKET-142, run against the agent's result.

The tests find the new function by trying the likely call shapes, so they do not depend on
the exact name the agent chose, only on the behaviour.
"""
import datetime as dt
import inspect
import unittest

import loyalty

TUE, SAT, SUN = dt.date(2026, 11, 3), dt.date(2026, 11, 7), dt.date(2026, 11, 8)


def call(total, tier, day):
    fn = getattr(loyalty, "points_for_order")
    params = list(inspect.signature(fn).parameters)
    kwargs = {}
    for name in params[1:]:
        low = name.lower()
        if "tier" in low or "level" in low or "member" in low:
            kwargs[name] = tier
        elif "date" in low or "day" in low or "when" in low or "at" == low:
            kwargs[name] = day
    if len(kwargs) == len(params) - 1:
        return fn(total, **kwargs)
    return fn(total, tier, day)


class Hidden(unittest.TestCase):
    def test_1_standard_weekday(self):
        self.assertEqual(call(1250, "standard", TUE), 120)

    def test_2_silver_weekday(self):
        self.assertEqual(call(1250, "silver", TUE), 180)

    def test_3_gold_weekday(self):
        self.assertEqual(call(1250, "gold", TUE), 240)

    def test_4_silver_weekend(self):
        self.assertEqual(call(1250, "silver", SAT), 360)

    def test_5_gold_weekend_capped(self):
        self.assertEqual(call(15000, "gold", SUN), 500)

    def test_7_under_a_pound(self):
        self.assertEqual(call(99, "gold", SAT), 0)


if __name__ == "__main__":
    unittest.main()
