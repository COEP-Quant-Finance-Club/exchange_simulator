class Order:
    def __init__(self, order_id, user, side, price, quantity, timestamp):
        self.order_id = order_id
        self.user = user
        self.side = side
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = quantity
        self.status = "NEW"
        self.timestamp = timestamp
    
    