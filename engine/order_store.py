from typing import List

from utils.file_io import *
from utils.serialization import *
from engine.order import Order


class OrderStore:
    """
    Handles persistence of active orders to disk and recovery on engine startup.

    Responsibility:
    - Save NEW and PARTIALLY_FILLED orders during graceful shutdown
    - Load persisted orders during engine startup
    - Reconstruct Order objects from stored data

    This class must NOT:
    - Perform order matching
    - Modify order state
    - Interact with sockets or clients
    """

    def __init__(self, filepath: str = "storage/orders_snapshot.json"):
        """
        Initialize the OrderStore.

        Parameters:
            filepath (str): Path to the JSON file used for
                            persisting active orders.
        """
        self.filepath = filepath

    def save(self, orders: List[Order]):
        """
        Persist active orders to disk.

        This method is expected to be called during:
        - Graceful engine shutdown

        Behavior:
        - Serialize only active orders (NEW or PARTIALLY_FILLED)
        - Write them as a snapshot to disk
        - Overwrite existing snapshot atomically
        """
        if not orders:
            return
        
        active_orders = [
            self.serialize_order(order)
            for order in orders
            if order.status in ("NEW", "PARTIALLY_FILLED")
        ]
    
        # ensure the directory should exist.
        directory = os.path.dirname(self.filepath)
        if directory:
            ensure_dir(directory)
        
        snapshot = {
            "version": 1,
            "orders": active_orders
        }

        save_json(self.filepath, snapshot)
    

    def load(self) -> List[Order]:
        """
        Load persisted orders from disk.

        This method is expected to be called during:
        - Engine startup before accepting new orders

        Behavior:
        - Read snapshot file if it exists
        - Deserialize stored data
        - Reconstruct Order objects
        - Return empty list if no snapshot exists
        """
        
        if not os.path.exists(self.filepath):
            return []
        
        data = load_json(self.filepath)
        order_data = data.get("orders", [])

        orders : List[Order] = []

        for order_dict in order_data:
            orders.append(self.deserialize_order(order_dict))



    def serialize_order(self, order: Order) -> dict:
        """
        Convert an Order object into a JSON-serializable dictionary.

        This isolates persistence schema from domain logic.
        """
        return order.to_dict()


    def deserialize_order(self, data: dict) -> Order:
        """
        Convert stored order data back into an Order object.

        Centralizes reconstruction logic to guarantee consistency.
        """
        return Order.from_dict(data=data)

    def clear(self):
        """
        Clear persisted order snapshot.

        Intended usage:
        - Testing
        - Manual resets
        """
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
