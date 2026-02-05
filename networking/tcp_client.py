import socket
import json

class TCPClient:
    """
    TCP client to send orders to the Exchange Engine and receive responses.
    Each client represents a single user session.
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
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print(f"Connection refused. Is the server running at {self.host}:{self.port}?")
            return False
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False

    def submit_order(self, order: dict) -> dict:
        """
        Send a single order to the engine and wait for response.
        
        Parameters:
            order (dict): Dictionary containing order details
                (user_id, side, quantity, price, type, etc.)
        
        Returns:
            dict: Engine response containing:
                - accepted (bool): whether the order was accepted
                - order_id (int): assigned by engine
                - trades (list): list of executed trades (may be empty)
                - remaining_quantity (int)
                - timestamp (float or str)
        
        Notes:
            - This method does NOT print anything.
            - Rendering of responses is handled by the interactive client layer.
        """
        if not self.sock:
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": "Not connected to server. Call connect() first."
            }
        
        try:
            # Serialize order to JSON and send
            message = json.dumps(order)
            self.sock.sendall(message.encode('utf-8'))
            self.sock.sendall(b'\n')  # Delimiter to mark end of message
            
            # Receive response from server
            response_data = b''
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                # Check if we received the complete message (ends with newline)
                if b'\n' in response_data:
                    break
            
            # Decode and parse JSON response
            response_str = response_data.decode('utf-8').strip()
            if response_str:
                response = json.loads(response_str)
                return response
            else:
                return {
                    "accepted": False,
                    "order_id": None,
                    "trades": [],
                    "remaining_quantity": order.get("quantity", 0),
                    "timestamp": None,
                    "error": "Empty response from server"
                }
                
        except json.JSONDecodeError as e:
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": f"Invalid JSON response: {e}"
            }
        except Exception as e:
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": f"Error submitting order: {e}"
            }

    def listen_updates(self):
        """
        Optional: Continuously listen for asynchronous updates
        from the engine (e.g., trades executed from other users).
        """
        if not self.sock:
            print("Not connected to server. Call connect() first.")
            return
        
        print("Listening for updates from server...")
        try:
            while True:
                data = self.sock.recv(4096)
                if not data:
                    print("Server closed connection")
                    break
                
                # Decode and parse JSON updates
                message = data.decode('utf-8').strip()
                if message:
                    try:
                        update = json.loads(message)
                        print(f"Received update: {update}")
                    except json.JSONDecodeError:
                        print(f"Received non-JSON message: {message}")
                        
        except KeyboardInterrupt:
            print("\nStopped listening for updates")
        except Exception as e:
            print(f"Error while listening: {e}")

    def close_connection(self):
        """
        Gracefully close the TCP connection.
        """
        if self.sock:
            try:
                self.sock.close()
                print("Connection closed")
            except Exception as e:
                print(f"Error closing connection: {e}")
            finally:
                self.sock = None
        else:
            print("No active connection to close")