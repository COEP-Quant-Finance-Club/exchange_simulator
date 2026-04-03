import random
from utils.logger import log_info
from utils.time_utils import current_timestamp

def generate_random_order():
    order_type = random.choice(["BUY", "SELL"])
    order_kind = random.choice(["LIMIT", "MARKET"])
    quantity = random.randint(1, 20)

    order = {
        "type": order_type,
        "kind": order_kind,
        "quantity": quantity,
        "timestamp": current_timestamp()
    }

    if order_kind == "LIMIT":
        order["price"] = random.randint(90, 110)

    return order

def run_simulation(n=10):
    log_info("Simulation started")

    for _ in range(n):
        order = generate_random_order()
        log_info(f"Generated Order: {order}")
        print(order)

    log_info("Simulation finished")

if __name__ == "__main__":
    run_simulation()

