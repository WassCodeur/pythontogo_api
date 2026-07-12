

def calculate_commission_amount(ticket_price: float, commission_percentage: float) -> float:
    """
    Calculate the commission amount based on the ticket price and commission percentage.

    Args:
        ticket_price (float): The price of the ticket.
        commission_percentage (float): The commission percentage.

    Returns:
        float: The calculated commission amount.
    """
    return float((ticket_price * commission_percentage) // 100)


if __name__ == "__main__":
    ticket_price = 100  # Example ticket price
    commission_percentage = 10  # Example commission percentage
    commission_amount = calculate_commission_amount(
        ticket_price, commission_percentage)
    print(f"Commission Amount: {commission_amount}")
