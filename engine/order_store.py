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

    def __init__(self, filepath: str = "orders.json"):
        """
        Initialize the OrderStore.

        Parameters:
            filepath (str): Path to the JSON file used for
                            persisting active orders.
        """
        pass

    def save(self, orders: list):
        """
        Persist active orders to disk.

        This method is expected to be called during:
        - Graceful engine shutdown
        - Optional periodic snapshots (if implemented later)

        Behavior:
        - Serialize only active orders (NEW or PARTIALLY_FILLED)
        - Write them as a snapshot to orders.json
        - Overwrite existing file content safely

        Parameters:
            orders (list): List of Order objects that are still active
        """
        pass

    def load(self) -> list:
        """
        Load persisted orders from disk.

        This method is expected to be called during:
        - Engine startup before accepting new orders

        Behavior:
        - Read orders.json if it exists
        - Deserialize stored data
        - Reconstruct Order objects with correct remaining quantities
        - Return an empty list if no persisted orders exist

        Returns:
            list: List of reconstructed Order objects
        """
        pass

    def serialize_order(self, order):
        """
        Convert an Order object into a JSON-serializable dictionary.

        This method exists to:
        - Isolate serialization logic
        - Ensure consistency of stored fields
        - Allow easy schema changes in the future

        Parameters:
            order (Order): Order instance to serialize

        Returns:
            dict: JSON-serializable representation of the order
        """
        pass

    def deserialize_order(self, data: dict):
        """
        Convert stored order data back into an Order object.

        This method exists to:
        - Centralize reconstruction logic
        - Guarantee correct restoration of order state
        - Avoid duplicating object creation logic elsewhere

        Parameters:
            data (dict): Dictionary loaded from orders.json

        Returns:
            Order: Reconstructed Order object
        """
        pass

    def clear(self):
        """
        Clear persisted order data.

        Intended usage:
        - Testing environments
        - Manual resets
        - After successful migration to another persistence layer

        This method should remove or reset the stored snapshot.
        """
        pass
