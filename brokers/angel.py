
import uuid
from datetime import datetime


def place_order(symbol, qty, side, order_type):
    return {
        "status": "success",
        "broker": "Angel One",
        "mode": "MOCK",
        "order_id": "ANG-" + str(uuid.uuid4())[:8].upper(),
        "symbol": symbol,
        "quantity": qty,
        "side": side,
        "order_type": order_type,
        "message": "Order placed successfully",
        "timestamp": datetime.now().isoformat()
    }
