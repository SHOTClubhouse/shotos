"""Stock control for the bakery's three shops."""

import csv


def reorder_level(daily_usage: float, lead_time_days: int, safety_days: int = 2) -> int:
    """Stock level at which to reorder: usage over the lead time plus safety stock, rounded up."""
    return int(daily_usage * lead_time_days + safety_days)
