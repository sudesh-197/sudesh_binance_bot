from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

def place_limit_order(client: Client, symbol, side, quantity, price):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )
        logging.info("✅ Limit order placed: %s", order)
        return order
    except BinanceAPIException as e:
        logging.error("❌ Limit order failed: %s", e)
        return {"error": str(e)}   # 👈 return error dict
    except Exception as e:
        logging.error("❌ Unexpected error: %s", e)
        return {"error": str(e)}
