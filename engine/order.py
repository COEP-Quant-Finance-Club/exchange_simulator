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

        # Order status: NEW → PARTIALLY_FILLED → FILLED
        self.status = "NEW"

    def apply_fill(self, filled_quantity: int):
        """
        Apply a fill to the order.

        Updates remaining quantity and status.
        This method must be called whenever a trade occurs.

        Parameters:
            filled_quantity (int): Quantity filled in a trade
        """
        pass

    def is_filled(self) -> bool:
        """
        Check if the order is fully filled.

        Returns:
            bool: True if remaining_quantity == 0
        """
        pass

    def is_active(self) -> bool:
        """
        Check if the order can still be matched.

        Returns:
            bool: True if order is not fully filled
        """
        pass

    def __repr__(self) -> str:
        """
        Developer-friendly string representation of the order.
        """
        pass
