
from brokers.angel import place_order as angel_order
from brokers.zerodha import place_order as zerodha_order
from brokers.samco import place_order as samco_order
from brokers.fivepaisa import place_order as fivepaisa_order


def place_order(broker, symbol, qty, side, order_type):

    broker = broker.lower().strip()

    if broker == "angel":
        return angel_order(symbol, qty, side, order_type)

    elif broker == "zerodha":
        return zerodha_order(symbol, qty, side, order_type)

    elif broker == "samco":
        return samco_order(symbol, qty, side, order_type)

    elif broker in ["fivepaisa", "5paisa"]:
        return fivepaisa_order(symbol, qty, side, order_type)

    else:
        raise ValueError(f"Unsupported broker: {broker}")

