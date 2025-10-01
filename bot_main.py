import sys
import argparse
from binance.client import Client
from market_orders import place_market_order
from limit_orders import place_limit_order
from utils import validate_quantity, validate_price, validate_symbol
import logging


API_KEY = "i5stEiRDl85hcXuEqfs86kf8L82kOdUdRDYywimyJG2idEdS46b2ewHMDssvGErN"
API_SECRET = "TvZh7MiNXYV1nrJDDg5HLasrxzI8OlIencNIXADryZLx8aLReE9VA65vCmIFna5h"

class BasicBot:
    def __init__(self, testnet=True):
        try:
            self.client = Client(API_KEY, API_SECRET, testnet=testnet)
            logging.info("✅ Bot initialized (Testnet=%s)", testnet)
        except Exception as e:
            logging.error("❌ Error initializing client: %s", str(e))
            raise

    def check_balance(self):
        balances = self.client.futures_account_balance()
        usdt = next((b for b in balances if b['asset'] == 'USDT'), None)
        return float(usdt["balance"]) if usdt else 0.0

def interactive_mode():
    print("⚡ Running in interactive mode (API keys are hardcoded)...")
    symbol = input("Enter Symbol (e.g. BTCUSDT): ").upper()
    side = input("Enter Side (BUY/SELL): ").upper()
    order_type = input("Enter Order Type (MARKET/LIMIT): ").upper()
    qty = float(input("Enter Quantity: "))

    bot = BasicBot(testnet=True)

    valid, err = validate_symbol(symbol)
    if not valid:
        print(err); return
    valid, err = validate_quantity(qty)
    if not valid:
        print(err); return

    if order_type == "MARKET":
        result = place_market_order(bot.client, symbol, side, qty)
    elif order_type == "LIMIT":
        price = float(input("Enter Price: "))
        valid, err = validate_price(price)
        if not valid:
            print(err); return
        result = place_limit_order(bot.client, symbol, side, qty, price)
    else:
        result = {"error": "❌ Invalid order type"}

    print("📌 Order Result:", result)


def cli_mode():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot (Testnet)")
    parser.add_argument("order_type", choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("symbol", help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price (required for LIMIT)")
    parser.add_argument("--testnet", action="store_true", help="Use Binance Futures Testnet")
    return parser.parse_args()


def main():
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        args = cli_mode()
        bot = BasicBot(testnet=args.testnet)

        valid, err = validate_symbol(args.symbol)
        if not valid: print(err); return
        valid, err = validate_quantity(args.quantity)
        if not valid: print(err); return

        if args.order_type == "MARKET":
            result = place_market_order(bot.client, args.symbol, args.side, args.quantity)
        elif args.order_type == "LIMIT":
            if not args.price:
                print("❌ Price required for LIMIT order"); return
            valid, err = validate_price(args.price)
            if not valid: print(err); return
            result = place_limit_order(bot.client, args.symbol, args.side, args.quantity, args.price)
        else:
            result = {"error": "❌ Invalid order type"}

        print("📌 Order Result:", result)

if __name__ == "__main__":
    main()
