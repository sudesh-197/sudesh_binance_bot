import logging

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def validate_quantity(quantity, min_qty=0.001):
    if quantity < min_qty:
        msg = f"❌ Invalid quantity: {quantity}. Must be >= {min_qty}"
        logging.warning(msg)
        return False, msg
    return True, None

def validate_price(price, min_price=1):
    if price < min_price:
        msg = f"❌ Invalid price: {price}. Must be >= {min_price}"
        logging.warning(msg)
        return False, msg
    return True, None

def validate_symbol(symbol, allowed_symbols=None):
    if allowed_symbols is None:
        allowed_symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    if symbol not in allowed_symbols:
        msg = f"❌ Invalid symbol: {symbol}. Allowed: {allowed_symbols}"
        logging.warning(msg)
        return False, msg
    return True, None
