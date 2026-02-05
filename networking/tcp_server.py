import socket
import threading
import json
from typing import Optional

class TCPServer:    
    """
    TCP server to accept orders from multiple clients and forward them
    to the ExchangeEngine. Each client runs in a separate thread 
    if implementation of the multithreaded is possible then do it 
    else stick to the singlethreaded request handling.
    """

    def __init__(self, host: str = "localhost", port: int = 9000, engine = None):
        """
        Initialize TCP server with host, port, and engine reference.
        """
        self.host = host
        self.port = port
        self.engine = engine
        self.server_socket = None
        self.client_threads = []
        self.running = False
        self.lock = threading.Lock()  # For thread-safe engine access

    def start_server(self):
        """
        Start the TCP server and begin listening for clients.

        Notes:
        - By the time this runs, the engine should already have restored
          the order book from any persisted JSON snapshot.
        - The server does not perform restoration itself.
        """
        try:
            # Create TCP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to host and port
            self.server_socket.bind((self.host, self.port))
            
            # Start listening for connections (backlog of 5)
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Server started on {self.host}:{self.port}")
            print("Waiting for client connections...")
            
            # Accept clients in a loop
            while self.running:
                try:
                    self.accept_client()
                except Exception as e:
                    if self.running:
                        print(f"Error accepting client: {e}")
                    
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            self.stop_server()

    def accept_client(self):
        """
        Accept a single incoming client connection and spawn a handler thread.
        """
        try:
            # Accept incoming connection
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from {client_address}")
            
            # Create and start a new thread to handle this client
            client_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
            
            # Keep track of client threads
            with self.lock:
                self.client_threads.append(client_thread)
                
        except OSError:
            # Socket was closed, stop accepting
            pass

    def handle_client(self, client_socket, client_address):
        """
        Receive orders from a client, forward to engine,
        and send back order confirmations/trade updates.

        Parameters:
            client_socket: Socket object for this client
            client_address: Client address tuple
        """
        print(f"Handling client {client_address}")
        
        try:
            buffer = b''
            
            while True:
                # Receive data from client
                data = client_socket.recv(4096)
                
                if not data:
                    # Client disconnected
                    print(f"Client {client_address} disconnected")
                    break
                
                buffer += data
                
                # Process complete messages (separated by newlines)
                while b'\n' in buffer:
                    # Extract one complete message
                    message, buffer = buffer.split(b'\n', 1)
                    
                    try:
                        # Decode and parse JSON
                        order = json.loads(message.decode('utf-8'))
                        print(f"Received order from {client_address}: {order}")
                        
                        # Forward to exchange engine
                        response = self.process_order(order)
                        
                        # Send response back to client
                        self.send_to_client(client_socket, response)
                        
                    except json.JSONDecodeError as e:
                        error_response = {"error": f"Invalid JSON: {e}"}
                        self.send_to_client(client_socket, error_response)
                    except Exception as e:
                        error_response = {"error": f"Error processing order: {e}"}
                        self.send_to_client(client_socket, error_response)
                        
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
        finally:
            # Clean up client connection
            try:
                client_socket.close()
            except:
                pass
            print(f"Connection with {client_address} closed")

    def process_order(self, order: dict) -> dict:
        """
        Forward order to the exchange engine and get response.
        Thread-safe execution using lock.
        
        Parameters:
            order (dict): Order details from client
            
        Returns:
            dict: Engine response with:
                - accepted (bool): whether the order was accepted
                - order_id (int): assigned by engine
                - trades (list): list of executed trades (may be empty)
                - remaining_quantity (int)
                - timestamp (float or str)
        """
        if not self.engine:
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": "Exchange engine not initialized"
            }
        
        try:
            # Thread-safe engine access
            with self.lock:
                # Call the engine's method to process the order
                # Assuming the engine has a method like place_order() or process_order()
                # Adjust this based on your actual engine implementation
                response = self.engine.place_order(order)
                return response
                
        except AttributeError:
            # If engine doesn't have the expected method, return error response
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": "Engine method 'place_order' not found"
            }
        except Exception as e:
            return {
                "accepted": False,
                "order_id": None,
                "trades": [],
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": None,
                "error": f"Engine error: {e}"
            }

    def send_to_client(self, client_socket, message: dict):
        """
        Send a dictionary message to the connected client.
        Typically used for order confirmations or trade execution updates.

        Parameters:
            client_socket: Socket object for this client
            message (dict): JSON-serializable data to send
        """
        try:
            # Serialize to JSON and send
            json_message = json.dumps(message)
            client_socket.sendall(json_message.encode('utf-8'))
            client_socket.sendall(b'\n')  # Message delimiter
            
        except Exception as e:
            print(f"Error sending to client: {e}")

    def stop_server(self):
        """
        Stop the server and gracefully close all client sockets.
        """
        print("Stopping server...")
        self.running = False
        
        # Close server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # Wait for all client threads to finish (with timeout)
        with self.lock:
            for thread in self.client_threads:
                if thread.is_alive():
                    thread.join(timeout=2.0)
        
        print("Server stopped")


# Standalone server runner (for testing)
if __name__ == "__main__":
    import time
    
    # Mock engine for testing
    class MockEngine:
        def __init__(self):
            self.order_counter = 1000
            
        def place_order(self, order):
            """Mock implementation matching expected response format"""
            self.order_counter += 1
            return {
                "accepted": True,
                "order_id": self.order_counter,
                "trades": [],  # No matching in mock - empty trades
                "remaining_quantity": order.get("quantity", 0),
                "timestamp": time.time()
            }
    
    # Create and start server
    engine = MockEngine()
    server = TCPServer(host="localhost", port=9000, engine=engine)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop_server()