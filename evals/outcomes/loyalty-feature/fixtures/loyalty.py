"""Loyalty points for the cafe chain's app."""

POINTS_PER_POUND = 10


def points_for_order(total_pence: int) -> int:
    """Points earned on an order: 10 points per whole pound spent."""
    return (total_pence // 100) * POINTS_PER_POUND
