import heapq

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
    
    def add_buy_orders(self, order):
        """
        this function will add the buy orders 
        return true if order is successfully added else return false
        """
        if order.side == "BUY":

            heapq.heappush(
                self.buy_orders,
                (-order.price, order.timestamp, order)
            )
            return True
        else:
            return False

    def add_sell_orders(self, order):
        """ 
        this function will add the sell orders
        return true if order is successfully added else return false
        """
        if order.side == "SELL":
            heapq.heappush(
                self.sell_orders,
                (order.price, order.timestamp, order)
            )
            return True
        else:
            return False
    
    def _match_buy(self, incoming_order):
        """
        this function will match the buy orders
        """
    
    def _match_sell(self, incoming_order):
        """
        this functionn will match the sell orders
        """
    