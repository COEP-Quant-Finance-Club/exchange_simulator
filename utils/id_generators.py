import uuid 

def generate_order_id():
    return uuid.uuid4().int % 10**15


def generate_client_id():
    return f"cli_{uuid.uuid4().hex[:8]}"

def generate_trade_id():
    return uuid.uuid4().int % 10 **17

print(generate_order_id())
print(generate_client_id())