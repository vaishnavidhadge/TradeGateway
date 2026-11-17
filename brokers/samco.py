
import uuid
from datetime import datetime


def place_order(symbol, qty, side, order_type):
    return {
        "status": "success",
        "broker": "Samco",
        "mode": "MOCK",
        "order_id": "SAM-" + str(uuid.uuid4())[:8].upper(),
        "symbol": symbol,
        "quantity": qty,
        "side": side,
        "order_type": order_type,
        "message": "Order placed successfully",
        "timestamp": datetime.now().isoformat()
    }
