class Order:
    """
    Represents a single limit or market order in the exchange.

    An Order is immutable in terms of price/side after creation.
    Only quantity-related fields and status may change during matching.
    """

    def __init__(
        self,
        order_id: int,
        user: str,
        side: str,
        quantity: int,
        price: float | None,
        timestamp: float,
        order_type: str = "LIMIT"
    ):
        """
        Initialize a new order.

        Parameters:
            order_id (int): Unique identifier for the order
            user (str): User who placed the order
            side (str): "BUY" or "SELL"
            quantity (int): Total quantity requested
            price (float | None): Limit price (None for market orders)
            timestamp (float): Order creation time
            order_type (str): "LIMIT" or "MARKET"
        """
        self.order_id = order_id
        self.user = user
        self.side = side
        self.price = price
        self.quantity = quantity
        self.remaining_quantity = quantity
        self.timestamp = timestamp
        self.order_type = order_type

        # Order status: NEW -> PARTIALLY_FILLED -> FILLED
        self.status = "NEW"

    def apply_fill(self, filled_quantity: int):
        """
        Apply a fill to the order.

        Updates remaining quantity and status.
        This method must be called whenever a trade occurs.
        ex:-
            if the order was originally had 10 quantity and now it has
            remaining quantities of < 10 & not equal to 0 then it should mark the
            order as PARTIALLY_FILLED and if it becomes 0 then FILLED
        Parameters:
            filled_quantity (int): Quantity filled in a trade
        """
        self.remaining_quantity -= filled_quantity
    
        # status update
        if  self.remaining_quantity == 0:
            self.status = "FILLED"
        else: 
            self.status = "PARTIALLY_FILLED"


    def is_filled(self) -> bool:
        """
        Check if the order is fully filled.

        Returns:
            bool: True if remaining_quantity == 0
        """
        if self.remaining_quantity == 0 :
            return True 
        else : 
            return False 
        
    

    def is_active(self) -> bool:
        """
        Check if the order can still be matched.

        Returns:
            bool: True if order is not fully filled
        """
        if self.remaining_quantity != 0:
            return True 
        else: 
            return False
        

    def to_dict(self) -> dict:
        """
        Convert this Order into a plain Python dictionary.

        Purpose:
        --------
        - Persistence
        - Network responses
        - Logging

        This method exposes internal state
        without leaking behavior.
        """
        return self.__dict__
        

    @classmethod
    def from_dict(cls, data: dict):
        """
        Reconstruct an Order from plain Python data.

        Used during:
        -------------
        - Engine restart
        - Order book recovery

        Assumes data has already been validated.
        """

        order = cls(
        order_id=data["order_id"],
        user=data["user"],
        side=data["side"],
        quantity=data["quantity"],
        price=data["price"],
        timestamp=data["timestamp"],
        order_type=data["order_type"]
        )

        order.remaining_quantity = data["remaining_quantity"]
        order.status = data["status"]

        return order

    def __repr__(self) -> str:
        """
        Developer-friendly string representation of the order.
        """
       
        return (
        f"Order(order_id={self.order_id}, "
        f"user={self.user!r}, "
        f"side={self.side!r}, "
        f"quantity={self.quantity}, "
        f"price={self.price}, "
        f"timestamp={self.timestamp}, "
        f"order_type={self.order_type!r})"
        )

import time
# testing 
if __name__ == "__main__":
    od = Order(order_id=12, user="Bhavesh", side="BUY", quantity=10, price=98.4, timestamp=time.time(), order_type="LIMIT")
    od.apply_fill(1)

    print(od.is_active())
    print(od.is_filled())
    odDict = od.to_dict()
    print(odDict)
    print()
    print(Order.from_dict(odDict))