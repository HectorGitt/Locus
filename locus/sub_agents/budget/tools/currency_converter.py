def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Converts currency.

    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency to convert from.
        to_currency (str): The currency to convert to.

    Returns:
        dict: A dictionary containing the converted amount.
    """
    # Mock conversion
    return {
        "converted_amount": f"{amount} {from_currency} is roughly equal to {amount * 1.1} {to_currency}."
    }
