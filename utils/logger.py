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
    print(f"DATE AND TIME: {get_formated_timestamp(trade["timestamp"])}")
    print(f"TRADE ID: {trade["trade_id"]}")
    print(f"PRICE: {trade["price"]}")
    print(f"QUANTITY: {trade["quantity"]}")
    print("")
    # print(f"REMAINING QUANTITIES: {trade["remaining_quantity"]}")
    