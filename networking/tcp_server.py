import socket
import threading
import json
from engine.engine import ExchangeEngine  # Engine class that does the matching

class TCPServer:
    """
    TCP server to accept orders from multiple clients and forward them
    to the ExchangeEngine. Each client runs in a separate thread 
    if implementation of the multithreaded is possible then do it 
    else stick to the singlethreaded request handling.
    
    """

    def __init__(self, host: str = "localhost", port: int = 9000, engine: ExchangeEngine = None):
        """
        Initialize TCP server with host, port, and engine reference.
        """
        self.host = host
        self.port = port
        self.engine = engine
        self.server_socket = None
        self.client_threads = []

    def start_server(self):
        """
        Start the TCP server and begin listening for clients.

        Notes:
        - By the time this runs, the engine should already have restored
          the order book from any persisted JSON snapshot.
        - The server does not perform restoration itself.

        """
        pass

    def accept_client(self):
        """
        Accept a single incoming client connection and spawn a handler thread.
        """
        pass

    def handle_client(self, client_socket, client_address):
        """
        Receive orders from a client, forward to engine,
        and send back order confirmations/trade updates.

        Parameters:
            client_socket: Socket object for this client
            client_address: Client address tuple
        """
        pass

    def send_to_client(self, client_socket, message: dict):
        """
        Send a dictionary message to the connected client.
        Typically used for order confirmations or trade execution updates.

        Parameters:
            client_socket: Socket object for this client
            message (dict): JSON-serializable data to send
        """
        pass

    def stop_server(self):
        """
        Stop the server and gracefully close all client sockets.
        
        """
        pass
