# run/start_engine.py

import sys
import os

# Ensure project root is on PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from engine.engine import ExchangeEngine
from engine.orderbook import OrderBook
from engine.trade_writer import TradeWriter
from networking.tcp_server import TCPServer


def main():
    print("[ENGINE] Starting exchange engine...")

    order_book = OrderBook()
    trade_writer = TradeWriter("storage/trades/trades.json")

    engine = ExchangeEngine(
        order_book=order_book,
        trade_writer=trade_writer
    )

    engine.start()

    server = TCPServer(
        host="0.0.0.0",
        port=9000,
        engine=engine
    )

    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n[ENGINE] Shutdown signal received")
    finally:
        server.stop()
        engine.stop()


if __name__ == "__main__":
    main()
