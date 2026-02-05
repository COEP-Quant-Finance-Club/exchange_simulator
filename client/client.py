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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

    def shutdown(self):
        """
        Gracefully shut down the client session.

        Responsibilities:
        - Close TCP connection
        - Flush or finalize session state if required
        - Print session termination message
        """
        pass
