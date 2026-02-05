"""
session_manager.py

Manages per-user session-level order history.

This module exists to:
- Persist a user's submitted orders locally
- Track order status transitions over time
- Provide session continuity across restarts

This module represents *client-side state only*.
"""

class SessionManager:
    """
    Manages local session order history for a single user.

    Design Notes:
    - Each user has their own session file:
        storage/session_orders/orders_userX.json
    - Orders are written optimistically as NEW
    - Status updates are applied after engine responses
    - The engine NEVER writes to these files

    This class acts as:
    - A local cache
    - A historical record
    """

    def __init__(self, user: str):
        """
        Initialize session manager for a user.

        Responsibilities:
        - Resolve user-specific session file path
        - Create session file if missing
        - Load existing session orders into memory

        Must NOT:
        - Communicate with engine
        - Perform validation of trading rules
        """
        pass

    def add_order(self, order: dict):
        """
        Add a newly submitted order to the session history.

        Responsibilities:
        - Store order with initial status = NEW
        - Persist order immediately to disk

        Notes:
        ------
        This method is called BEFORE the engine responds.
        """
        pass

    def update_order(self, response: dict):
        """
        Update order state based on engine response.

        Responsibilities:
        - Update order status:
            NEW -> PARTIALLY_FILLED
            PARTIALLY_FILLED -> FILLED
        - Update remaining quantity
        - Append trade execution details if present

        Assumptions:
        ------------
        - Response contains authoritative order_id and status
        - Engine is the source of truth for execution outcomes
        """
        pass

    def load_orders(self):
        """
        Load existing session orders from disk.

        Responsibilities:
        - Read session JSON file
        - Reconstruct in-memory order list

        Used when:
        - Client restarts
        - Session resumes
        """
        pass

    def save(self):
        """
        Persist current session state to disk.

        Responsibilities:
        - Write full order list to session JSON file
        - Ensure file integrity

        Must NOT:
        - Block user interaction unnecessarily
        """
        pass
