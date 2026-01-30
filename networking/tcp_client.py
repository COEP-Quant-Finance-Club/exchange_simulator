import socket
import json

class TCPClient:
    """
    TCP client to send orders to the Exchange Engine and receive responses.
    Each client represents a single user ses  sion.
    """

    def __init__(self, host: str = "localhost", port: int = 9000):
        """
        Initialize TCP client with host and port.
        """
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        """
        Establish a TCP connection to the engine.

        Notes:
        - Engine is assumed to have its order book restored and ready.
        - This method does not trigger restoration.
.
        """
        pass

    def submit_order(self, order: dict) -> dict:
        """
        Send a single order to the engine and wait for response.

        Parameters:
            order (dict): Dictionary containing order details
                (user_id, side, quantity, price, type, etc.)

        Returns:
            dict: Engine response including:
                  - Order confirmation
                  - Partial or full fills
                  - Trade execution details
        """
        pass

    def listen_updates(self):
        """
        Optional: Continuously listen for asynchronous updates
        from the engine (e.g., trades executed from other users).
        """
        pass

    def close_connection(self):
        """
        Gracefully close the TCP connection.
        """
        pass
