"""Basket pricing for the online shop."""

VAT_RATE = 0.20


def line_total(unit_price_pence: int, quantity: int) -> int:
    """Price of one basket line before discounts, in pence."""
    return unit_price_pence * quantity


def apply_discount(subtotal_pence: int, code: str | None) -> int:
    """Apply a discount code. SAVE10 takes 10% off; FIVER takes 500p off orders of 2500p or more."""
    if code == "SAVE10":
        return round(subtotal_pence * 0.9)
    if code == "FIVER" and subtotal_pence > 2500:
        return subtotal_pence - 500
    return subtotal_pence


def basket_total(lines: list[tuple[int, int]], code: str | None = None) -> int:
    """Total to charge in pence, VAT included. Prices in the catalogue exclude VAT."""
    subtotal = sum(line_total(price, qty) for price, qty in lines)
    discounted = apply_discount(subtotal, code)
    return round(discounted * VAT_RATE)
