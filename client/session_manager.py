"""
session_manager.py

Manages per-user session-level order history.

This module exists to:
- Persist a user's submitted orders locally
- Track order status transitions over time
- Provide session continuity across restarts

This module represents *client-side state only*.
"""
import os
import json
import atexit

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
        if not isinstance(user, str) or not user.strip():
            raise ValueError("Invalid username")

        self.user = user.strip().replace(" ", "_")

        self.dir_path = os.path.join("storage", "session_orders")
        os.makedirs(self.dir_path, exist_ok=True)

        self.file_path = os.path.join(self.dir_path, f"orders_{self.user}.json")

        # Making sure only one user per username is active
        self.lock_path = os.path.join(self.dir_path, f"{self.user}.lock")

        if os.path.exists(self.lock_path):
            raise RuntimeError(
                f"User '{self.user}' already has an active session"
            )

        with open(self.lock_path, "w") as f:
            f.write("active")

        atexit.register(self.release_lock)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

        self.orders = []
        self.load_orders()


    def release_lock(self):
        """
        Remove lock file on shutdown.

        Prevents permanent lock if program exits cleanly.
        """
        if os.path.exists(self.lock_path):
            os.remove(self.lock_path)


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

        if not isinstance(order, dict):
            raise ValueError("Order must be dict")

        qty = order.get("quantity")

        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Invalid quantity")

        record = dict(order)

        record["status"] = "NEW"
        record["remaining_quantity"] = record.get("quantity", 0)
        record["trades"] = []

        self.orders.append(record)

        self.save()

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

        order_id = response.get("order_id")
        if order_id is None:
            return

        target = None

        for o in self.orders:
            if o.get("order_id") == order_id:
                target = o
                break

        if target is None:
            for o in reversed(self.orders):
                if "order_id" not in o:
                    o["order_id"] = order_id
                    target = o
                    break

        if target is None:
            return

        if "remaining_quantity" in response:
            target["remaining_quantity"] = response["remaining_quantity"]

        rq= target["remaining_quantity"]
        q = target.get("quantity", 0)

        if rq == 0:
            target["status"] = "FILLED"

        elif 0 < rq < q:
            target["status"] = "PARTIALLY_FILLED"

        if response.get("trades"):
            target.setdefault("trades", [])
            target["trades"].extend(response["trades"])

        self.save()


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
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.orders = data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            self.orders = []


    def save(self):
        """
        Persist current session state to disk.

        Responsibilities:
        - Write full order list to session JSON file
        - Ensure file integrity

        Must NOT:
        - Block user interaction unnecessarily
        """

        tmp_path = self.file_path + ".tmp"

        with open(tmp_path, "w") as f:
            json.dump(self.orders, f, indent=2)

        os.replace(tmp_path, self.file_path)
