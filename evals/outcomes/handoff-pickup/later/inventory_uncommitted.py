"""Stock control for the bakery's three shops."""

import csv


def reorder_level(daily_usage: float, lead_time_days: int, safety_days: int = 2) -> int:
    """Stock level at which to reorder: usage over the lead time plus safety stock, rounded up."""
    return int(daily_usage * lead_time_days + safety_days)


def load_stock(path: str) -> dict:
    """Read stock.csv into {item: quantity}."""
    with open(path, newline="", encoding="utf-8") as f:
        return {row["item"]: int(row["quantity"]) for row in csv.DictReader(f)}
