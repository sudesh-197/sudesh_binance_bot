from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

def place_market_order(client: Client, symbol, side, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        logging.info("✅ Market order placed: %s", order)
        return order
    except BinanceAPIException as e:
        logging.error("❌ Market order failed: %s", e)
        return {"error": str(e)}   # 👈 return error dict
    except Exception as e:
        logging.error("❌ Unexpected error: %s", e)
        return {"error": str(e)}
