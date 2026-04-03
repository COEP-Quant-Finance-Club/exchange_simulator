class Trade:
    def __init__(self, trade_id, buy_order_id, sell_order_id, buy_client_id, sell_client_id, price, quantity, timestamp):
        self.trade_id = trade_id
        self.buy_order_id = buy_order_id
        self.sell_order_id = sell_order_id
        self.buy_client_id = buy_client_id
        self.sell_client_id = sell_client_id
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp
   
    
    def to_dict(self) -> dict:
        """
        Convert Trade into a plain dictionary.

        Used for:
        - JSON persistence
        - Network responses
        - Logging
        """
        return {
            "trade_id": self.trade_id,
            "buy_order_id": self.buy_order_id,
            "sell_order_id": self.sell_order_id,
            "buy_client_id": self.buy_client_id,
            "sell_client_id": self.sell_client_id,
            "price": self.price,
            "quantity": self.quantity,
            "timestamp": self.timestamp,
        }


    @classmethod
    def from_dict(cls, data: dict) -> "Trade":
        """
        Reconstruct a Trade from persisted data.

        Assumes data is already validated.
        """
        return cls(
            trade_id=data["trade_id"],
            buy_order_id=data["buy_order_id"],
            sell_order_id=data["sell_order_id"],
            buy_client_id=data["buy_client_id"],
            sell_client_id=data["sell_client_id"],
            price=data["price"],
            quantity=data["quantity"],
            timestamp=data["timestamp"],
        )

    def __repr__(self) -> str:
        return (
            f"Trade(trade_id={self.trade_id}, "
            f"buy_order_id={self.buy_order_id}, "
            f"sell_order_id={self.sell_order_id}, "
            f"buy_client_id= {self.buy_client_id}, "
            f"sell_client_id={self.sell_client_id}, "
            f"price={self.price}, "
            f"quantity={self.quantity}, "
            f"timestamp={self.timestamp})"
        )
