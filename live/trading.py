# This is a mock trading service.
# TODO: Replace this with the actual Motilal Oswal API integration.

import json
import os
from live.api import place_order as api_place_order

POSITIONS_FILE = "positions.json"

def place_order(symbol, signal, price, target_price):
    """Places a new order."""
    order_id = api_place_order(symbol, signal, price, target_price)
    order = {
        "order_id": order_id,
        "symbol": symbol,
        "signal": signal,
        "price": price,
        "target_price": target_price,
        "status": "open",
    }
    _save_position(order)
    print(f"Placed order for {symbol} at {price} with target {target_price}")
    return order

def get_order_status(order_id):
    """Gets the status of an order."""
    positions = _get_positions()
    if order_id < len(positions):
        return positions[order_id]
    return None

def cancel_order(order_id):
    """Cancels an order."""
    positions = _get_positions()
    if order_id < len(positions):
        positions.pop(order_id)
        _save_positions(positions)
        print(f"Cancelled order {order_id}")
        return True
    return False

def _get_positions():
    """Gets all open positions."""
    if not os.path.exists(POSITIONS_FILE):
        return []
    with open(POSITIONS_FILE, "r") as f:
        return json.load(f)

def _save_positions(positions):
    """Saves all open positions."""
    with open(POSITIONS_FILE, "w") as f:
        json.dump(positions, f, indent=4)

def _save_position(position):
    """Saves a single position."""
    positions = _get_positions()
    positions.append(position)
    _save_positions(positions)
