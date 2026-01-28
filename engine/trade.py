class Trade:
    def __init__(self, trade_id, buy_order_id, sell_order_id, price, quantity, timestamp):
        self.trade_id = trade_id
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp
    