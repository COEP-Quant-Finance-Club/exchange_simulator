
from engine.engine import ExchangeEngine
from engine.orderbook import OrderBook
from engine.order_store import OrderStore
from engine.trade_writer import TradeWriter
from networking.tcp_server import TCPServer


def main():
    print("[SERVER] Starting Exchange Engine...")

    # core components
    order_store = OrderStore()
    order_book = OrderBook(order_store=order_store)
    trade_writer = TradeWriter(
        ledger_path="storage/trades/trades.json"
    )
    trade_writer.start()

    engine = ExchangeEngine(
        order_book=order_book,
        trade_writer=trade_writer,
        logger=None
    )


    engine.start()

    #TCP Server 
    server = TCPServer(
        host="0.0.0.0",
        port=9000,
        engine=engine
    )

    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n[SERVER] Shutdown requested")
    finally:
        print("[SERVER] Shutting down...")

        server.stop_server()
        engine.stop()
        trade_writer.stop()


if __name__ == "__main__":
    main()
