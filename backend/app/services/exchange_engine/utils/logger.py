from utils.time_utils import *
from utils.file_io import ensure_dir, ensure_file
LOG_FILE = "storage/logs/system.log"

def _prepare_log_file():
    ensure_dir("storage/logs")
    ensure_file(LOG_FILE)

def log_info(message):
    _prepare_log_file()
    with open(LOG_FILE, "a") as f:
        f.write(f"[INFO] {current_timestamp()} - {message}\n")

def log_trade_system(trade):
    _prepare_log_file()
    with open(LOG_FILE, "a") as f:
        f.write(f"[TRADE] {current_timestamp()} - {trade}\n")

def log_error(message):
    _prepare_log_file()
    with open(LOG_FILE, "a") as f:
        f.write(f"[ERROR] {current_timestamp()} - {message}\n")
    
def log_trade_client(trade):
    """Log the trade at client side."""
    print(f"DATE AND TIME: {get_formated_timestamp(trade["timestamp"])}")
    print(f"TRADE ID: {trade["trade_id"]}")
    print(f"PRICE: {trade["price"]}")
    print(f"QUANTITY TRADED: {trade["quantity"]}")
    print()
    # print(f"REMAINING QUANTITIES: {trade["remaining_quantity"]}")

def log_trade_server(trade):
    """Log the trade at server side."""
    print("\n[SERVER] Trade Executed")
    print(f"Trade ID: {trade.trade_id}")
    print(f"Time: {get_formated_timestamp(trade.timestamp)}")
    print(f"Buy Order ID: {trade.buy_order_id}")
    print(f"Sell Order ID: {trade.sell_order_id}")
    print(f"Price: {trade.price}")
    print(f"Quantity: {trade.quantity}")
    print()

def log_received_order(client_address, order):
    ip, port = client_address

    order_type = order.get("order_type", "UNKNOWN")
    price = order.get("price", 0)

    price_display = "MARKET" if order_type == "MARKET" or price == 0 else price

    print("\n[SERVER] Order Received")
    print(f"Client      : {order.get('client_id')} ({order.get('user')})")
    print(f"Address     : {ip}:{port}")
    print(f"Side        : {order.get('side')}")
    print(f"Type        : {order_type}")
    print(f"Quantity    : {order.get('quantity')}")
    print(f"Price       : {price_display}")
    print(f"Status      : {order.get('status')}")
    print()
