import heapq
from engine.trade import Trade
from engine.order import Order
import time
class OrderBook:
    def __init__(self):
        # this will store the pending orders
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
    
    def _match_limit_buy(self, incoming_order):
        """
        Match an incoming BUY limit order against the sell order book
        using price-time priority.
        The function continuously matches the incoming BUY order with the
        best available SELL orders (lowest price, earliest timestamp) as long as:
          - The incoming order has remaining quantity, and
          - The best sell price is less than or equal to the buy price.
        For each successful match:
          - A trade is executed at the sell order price
          - Order quantities are updated
          - Fully filled sell orders are removed from the order book
          - A Trade object is created and recorded
        Parameters:
            incoming_order (Order): The incoming BUY limit order to be matched.
        Returns:
            list[Trade]: A list of Trade objects generated from the matching
            process. The list may be empty if no matches occur.
        """
        trades = []
        
        while incoming_order.remaining_quantity > 0 and self.sell_orders: 
            # get the best sell order
            
            best_sell_price, best_sell_timestamp, best_sell_order  = self.sell_orders[0]
            if best_sell_price <= incoming_order.price:
                
                #get the trade quantity
                trade_quantity = min(best_sell_order.remaining_quantity, incoming_order.remaining_quantity)
                # this statements will be replaced with the methods(function) calls in the order.py class
                # incoming_order.remaining_quantity -= trade_quantity
                # best_sell_order.remaining_quantity -= trade_quantity
               
                incoming_order.apply_fill(trade_quantity)
                best_sell_order.apply_fill(trade_quantity)
                
                # get the current timestamp
                curr_timestamp = time.time()
                
                #creation of Trade of object
                trade = Trade(buy_order_id=incoming_order.order_id,
                      sell_order_id=best_sell_order.order_id,
                        price=best_sell_price,
                        quantity=trade_quantity,
                        timestamp=curr_timestamp)
                
                #appending that object in the trades array
                trades.append(trade)
                
                # remove the order
                if best_sell_order.remaining_quantity == 0:
                    heapq.heappop(self.sell_orders)
                
            else:
                break
        return trades
            

    
    def _match_limit_sell(self, incoming_order):
        """
        Match an incoming SELL limit order against the buy order book
        using price-time priority.

        The function continuously matches the incoming SELL order with the
        best available BUY orders (highest price, earliest timestamp) as long as:
        - The incoming order has remaining quantity, and
        - The best buy price is greater than or equal to the sell price.

        For each successful match:
        - A trade is executed at the buy order price
        - Order quantities are updated
        - Fully filled buy orders are removed from the order book
        - A Trade object is created and recorded

        Parameters:
            incoming_order (Order): The incoming SELL limit order to be matched.

        Returns:
            list[Trade]: A list of Trade objects generated from the matching
            process. The list may be empty if no matches occur.

        """
        trades = []
        while incoming_order.remaining_quantity > 0 and self.buy_orders:
            best_buy_price, best_buy_timestamp, best_buy_order = self.buy_orders[0]
            best_buy_price = -1 * best_buy_price
            if best_buy_price >= incoming_order.price:
                
                # get the trade quantity
                trade_quantity = min(best_buy_order.remaining_quantity, incoming_order.remaining_quantity)
                
                #this statements will be replaced with the methods(function) calls in the order.py
                # incoming_order.remaining_quantity -= trade_quantity
                # best_buy_order.remaining_quantity -= trade_quantity
                incoming_order.apply_fill(trade_quantity)
                best_buy_order.apply_fill(trade_quantity)
                
                # get the current timestamp
                curr_timestamp = time.time()
                
                #creation of Trade of object
                trade = Trade(buy_order_id=best_buy_order.order_id,
                      sell_order_id=incoming_order.order_id,
                        price=best_buy_price,
                        quantity=trade_quantity,
                        timestamp=curr_timestamp)
                
                #appending that object in the trades array
                trades.append(trade)
                
                # remove the order
                if best_buy_order.remaining_quantity == 0:
                    heapq.heappop(self.buy_orders)
                
            else:
                break
        return trades
    
    def process_limit_order(self, incoming_order):
        """
        Process an incoming limit order:
        - Attempt to match it against the opposite order book
        - Insert it into the order book if partially filled or unfilled

        Returns:
            list[Trade]: Trades generated during matching
        """
        
        if incoming_order.side == "BUY":
            trades = self._match_limit_sell(incoming_order)
            if incoming_order.remaining_quantity > 0:
                self.add_buy_orders(incoming_order)
        
        elif incoming_order.side == "SELL":
            trades = self._match_limit_buy(incoming_order)
            if incoming_order.remaining_quantity > 0:
                self.add_sell_orders(incoming_order)
        return trades
    
    @staticmethod
    def to_dict(self) -> dict:
        """
        Convert the entire order book into a plain Python dictionary.

        Purpose:
        --------
        - Snapshot persistence on shutdown

        Delegates serialization of individual orders
        to Order.to_dict().
        """
        return {
            "buy_orders": [
                order.to_dict() for (_, _, order) in self.buy_orders
            ],
            "sell_orders": [
                order.to_dict() for (_, _, order) in self.sell_orders
            ]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Restore an OrderBook from persisted snapshot data.

        Used only during engine startup.
        """
        order_book = cls()

        for order_data in data.get("buy_orders", []):
            order = Order.from_dict(order_data)
            order_book.add_buy_orders(order)

        for order_data in data.get("sell_orders", []):
            order = Order.from_dict(order_data)
            order_book.add_sell_orders(order)

        return order_book

    def _match_market_buy(self, incoming_order):
        """
        Match an incoming buy limit order against the sell order book
        using price-time priority.

        The function continuously excutes the incoming buy order with the
        current available BUY orders (highest price, earliest timestamp) as long as:
        - The incoming order has remaining quantity
        
        Returns: 
            list[Trade]: Trades generated during running of this function
        """

        trades = []

        while incoming_order.remaining_quantity > 0 and self.sell_orders:
            best_sell_price, best_sell_timestamp, best_sell_order = self.sell_orders[0]
            trade_quantity = min(best_sell_order.remaining_quantity, incoming_order.remaining_quantity)

            # this statements will be replaced with the methods(function) calls in the order.py class
            # incoming_order.remaining_quantity -= trade_quantity
            # best_sell_order.remaining_quantity -= trade_quantity
            
            incoming_order.apply_fill(trade_quantity)
            best_sell_order.apply_fill(trade_quantity)
            
            # get the current timestamp
            curr_timestamp = time.time()
            
            #creation of Trade of object
            trade = Trade(buy_order_id=incoming_order.order_id,
                  sell_order_id=best_sell_order.order_id,
                    price=best_sell_price,
                    quantity=trade_quantity,
                    timestamp=curr_timestamp)
            
            #appending that object in the trades array
            trades.append(trade)
            # remove the order
            if best_sell_order.remaining_quantity == 0:
                heapq.heappop(self.sell_orders)
        
        return trades
    
    def _match_market_sell(self, incoming_order):
        """
        Match an incoming SELL market order against the buy order book
        using price-time priority.

        The function continuously excutes the incoming SELL order with the
        current available BUY orders (highest price, earliest timestamp) as long as:
        - The incoming order has remaining quantity
        
        Returns: 
            list[Trade]: Trades generated during running of this function
        
        """
        trades = []

        while incoming_order.remaining_quantity > 0 and self.buy_orders:
            
            best_buy_price, best_buy_timestamp, best_buy_order = self.buy_orders[0]
            best_buy_price = -1 * best_buy_price
            
            # get the trade quantity
            trade_quantity = min(best_buy_order.remaining_quantity, incoming_order.remaining_quantity)
            
            #this statements will be replaced with the methods(function) calls in the order.py
            # incoming_order.remaining_quantity -= trade_quantity
            # best_buy_order.remaining_quantity -= trade_quantity
            
            incoming_order.apply_fill(trade_quantity)
            best_buy_order.apply_fill(trade_quantity)
            # get the current timestamp
            curr_timestamp = time.time()
            #creation of Trade of object
            trade = Trade(buy_order_id=best_buy_order.order_id,
                  sell_order_id=incoming_order.order_id,
                    price=best_buy_price,
                    quantity=trade_quantity,
                    timestamp=curr_timestamp)
            
            #appending that object in the trades array
            trades.append(trade)
            
            # remove the order
            if best_buy_order.remaining_quantity == 0:
                heapq.heappop(self.buy_orders)
        return trades
            
    
    def process_market_orders(self, incoming_order):
        """
        Process an incoming market order:
        - Attempt to match it against the opposite order book
        - Insert it into the order book if partially filled or unfilled

        Returns:
            list[Trade]: Trades generated during matching
        """
        
        if incoming_order.side == "BUY":
            trades = self._match_market_sell(incoming_order)
            if incoming_order.remaining_quantity > 0:
                self.add_buy_orders(incoming_order)
        
        elif incoming_order.side == "SELL":
            trades = self._match_market_buy(incoming_order)
            if incoming_order.remaining_quantity > 0:
                self.add_sell_orders(incoming_order)
        
        return trades
    
    def snapshot(self) -> dict:
        """
        Create a serializable snapshot of the current order book state.

        Includes:
        - All active BUY orders
        - All active SELL orders

        Excludes:
        - Filled orders
        - Trade history

        Returns:
            dict: Snapshot suitable for JSON persistence
        """
        buy_orders = []
        sell_orders = []

        # BUY heap: (-price, timestamp, Order)
        for _, _, order in self.buy_orders:
            if order.is_active():
                buy_orders.append(order.to_dict())

        # SELL heap: (price, timestamp, Order)
        for _, _, order in self.sell_orders:
            if order.is_active():
                sell_orders.append(order.to_dict())

        return {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }
    

    def restore(self, snapshot: dict) -> None:
        """
        Restore order book state from a snapshot.

        Parameters:
            snapshot (dict): Output from snapshot()

        Notes:
        - Clears existing order book
        - Rebuilds BUY and SELL heaps
        - Preserves price-time priority
        """
        self.buy_orders.clear()
        self.sell_orders.clear()

        # Restore BUY orders
        for order_data in snapshot.get("buy_orders", []):
            order = Order.from_dict(order_data)
            heapq.heappush(
                self.buy_orders,
                (-order.price, order.timestamp, order)
            )

        # Restore SELL orders
        for order_data in snapshot.get("sell_orders", []):
            order = Order.from_dict(order_data)
            heapq.heappush(
                self.sell_orders,
                (order.price, order.timestamp, order)
            )

