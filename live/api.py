# This is a mock API for the Motilal Oswal trading platform.
# TODO: Replace this with the actual API integration.

import random

def place_order(symbol, signal, price, target_price):
    """Places a new order and returns an order ID."""
    print(f"Placing order for {symbol} at {price} with target {target_price}")
    return random.randint(1000, 9999)

def get_order_status(order_id):
    """Gets the status of an order."""
    # In a real scenario, this would make an API call to get the order status.
    # For this mock API, we'll just return a random status.
    statuses = ["open", "executed", "cancelled"]
    return random.choice(statuses)

def get_trade_history():
    """Gets the trade history for the day."""
    # In a real scenario, this would make an API call to get the trade history.
    # For this mock API, we'll just return a list of mock trades.
    return [
        {"symbol": "RELIANCE.NS", "price": 2800, "status": "executed"},
        {"symbol": "TCS.NS", "price": 3500, "status": "executed"},
    ]
