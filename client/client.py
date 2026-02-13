"""
client.py

Terminal-based client application for the Exchange Simulator.

This module is responsible ONLY for:
- Interacting with the user via terminal input/output
- Validating user input at the client boundary
- Coordinating with networking and session layers

This file is intentionally a *dumb UI layer*.
It must NOT contain:
- Matching logic
- Order ID generation
- Order book manipulation
- Persistence logic
"""
from utils.logger import *
import argparse
import questionary
from utils.id_generators import generate_client_id
from client.session_manager import SessionManager
from networking.tcp_client import TCPClient


class ClientUI:
    """
    Terminal-based user interface for a single trading session.

    Design Notes:
    - Each instance represents one user session.
    - The client is interactive and blocking (terminal-driven).
    - The client does NOT react asynchronously to engine events.
      Trade execution messages are displayed ONLY after:
        - The user finishes submitting an order
        - The engine responds to that submission

    Important UX Rule:
    -----------------
    While the user is in the middle of creating an order
    (entering side, quantity, price, etc.),
    NO trade execution messages should be printed to the terminal.

    All engine responses are handled *after* order submission completes.
    """

    def __init__(self, user: str, host: str = "localhost", port: int = 9000):
        """
        Initialize the client UI for a specific user.

        Responsibilities:
        - Store user identity
        - Initialize networking client
        - Initialize session manager

        Must NOT:
        - Open sockets directly
        - Load or write files
        """

        self.user = user
        self.session = SessionManager(self.user)
        self.tcp_client = TCPClient(host, port)


    def start(self):
        """
        Start the interactive client loop.

        Responsibilities:
        - Display welcome message
        - Repeatedly prompt the user for new orders
        - Gracefully handle user exit (e.g., Ctrl+C or 'exit')
        - Delegate order submission and response handling

        This method controls the lifecycle of the session.
        """

        print(f"Welcome to the Exchange Simulator ,{self.user}")

        if not self.tcp_client.connect():
            print("Connection failed")
            return

        try:
            while True:
                order = self._prompt_order()
                if order is None:
                    break

                self.session.add_order(order)
                response = self.tcp_client.submit_order(order)
                self._handle_response(response)

        except KeyboardInterrupt:
            print("User interrupted")

        finally:
            self.shutdown()


    def _prompt_order(self):
        """
        Prompt the user to create a new order via terminal input.

        Responsibilities:
        - Ask for order side (BUY / SELL)
        - Ask for order type (LIMIT / MARKET)
        - Ask for quantity
        - Ask for price (LIMIT orders only)

        Client-Side Validation Rules:
        -----------------------------
        - Quantity must be > 0
        - Price must be > 0 for LIMIT orders
        - Side must be BUY or SELL
        - Order type must be LIMIT or MARKET

        Invalid inputs should be:
        - Detected immediately
        - Rejected before sending anything to the engine

        Returns:
        - A validated order dictionary
        - OR None if the user chooses to exit
        """

        proceed = questionary.select(
            "Would you like to proceed?",
            choices = ["Yes", "No"],
        ).ask()

        if proceed != "Yes":
            return None

        side = questionary.select(
            "Order side:",
            choices=["BUY", "SELL"]
        ).ask()

        otype = questionary.select(
            "Order type:",
            choices=["LIMIT", "MARKET"]
        ).ask()

        qty_str = questionary.text(
            "Quantity:",
            validate=lambda x: x.isdigit() and int(x) > 0
        ).ask()

        quantity = int(qty_str)

        price = None

        if otype == "LIMIT":
            price_str = questionary.text(
                "Price:",
                validate=lambda x: x.isdigit() and int(x) > 0
            ).ask()
            price = int(price_str)

        order = {
            "user": self.user,
            "side": side,
            "order_type": otype,
            "status": "NEW",
            "quantity": quantity,
            "client_id": generate_client_id()
        }

        if price is not None:
            order["price"] = price

        return order

    def _submit_order(self, order: dict):
        """
        Send a validated order to the engine via the TCP client.

        Responsibilities:
        - Serialize and send order
        - Block until engine response is received

        Must NOT:
        - Modify order contents
        - Generate IDs or timestamps
        """
        return self.tcp_client.submit_order(order)



    def _handle_response(self, response: dict):
        """
        Handle engine response after order submission completes.

        Responsibilities:
        - Display order acceptance or rejection
        - Display trade execution details (if any)
        - Display remaining quantity and order status
        - Delegate session-level updates to SessionManager

        Important:
        ----------
        This method is the ONLY place where trade execution
        messages are printed to the terminal.
        """


        print("\n--- Engine Response ---")

        if not response.get("accepted", True):
            print("Order rejected")
            print(response)
            return
        
        # print(response)

        self.session.update_order(response)

        print("Order accepted")
        print("Order ID:", response.get("order_id"))

        trades = response.get("trades") or []
        if trades:
            print("\nTrades executed:")
            for t in trades:
                log_trade_system(t)
                log_trade_client(t)


    def shutdown(self):
        """
        Gracefully shut down the client session.

        Responsibilities:
        - Close TCP connection
        - Flush or finalize session state if required
        - Print session termination message
        """
        self.tcp_client.close_connection()
        self.session.release_lock()
        print("\nSession closed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9000)

    args = parser.parse_args()

    ClientUI(args.user, args.host, args.port).start()

