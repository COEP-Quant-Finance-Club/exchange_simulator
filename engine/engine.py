import time
from typing import Dict, List, Optional, Tuple
import uuid
from engine.trade import Trade
from engine.order import Order

class ExchangeEngine:
    """
    Central matching engine of the exchange.

    Responsibilities:
    - Validate incoming orders
    - Assign unique order IDs
    - Route orders to the order book
    - Generate trades
    - Produce client-facing responses
    - Emit execution events for logging / persistence

    This class contains *business logic only*.
    No networking, no threading, no printing.
    """

    def __init__(self, order_book=None, logger=None):
        """
        Initialize the exchange engine.

        Parameters:
            order_book:
                Component responsible for storing and matching orders.
                Must expose matching APIs (to be defined later).

            logger:
                Optional logger for audit trail and persistence.
        """
        self.order_book = order_book
        self.logger = logger

        self._order_id_counter = 0
        self._running = False

    def start(self) -> None:
        """
        Start the exchange engine.

        Called once during system bootstrap.
        Useful for:
        - Loading persisted state
        - Initializing metrics
        """
        self._running = True

    def stop(self) -> None:
        """
        Gracefully stop the exchange engine.

        Useful for:
        - Persisting order book state
        - Flushing logs
        """
        self._running = False
        

    def place_order(self, incoming_order: Dict) -> Dict:
        """
        Main entry point for all incoming client orders.

        Flow:
            1. Validate order
            2. Assign order_id
            3. Match order via order book
            4. Generate trades
            5. Build response for client

        Parameters:
            order (dict):
                Raw order data from client.

        Returns:
            dict:
                Client-facing response:
                {
                    "accepted": bool,
                    "order_id": int | None,
                    "trades": list,
                    "remaining_quantity": int,
                    "timestamp": float,
                    "message": str
                }
        """
        # validate the order
        try:
            # 0. Engine must be running
            self._assert_engine_running()

            # 1. Validate incoming order
            self._validate_order(incoming_order)

            # 2. Assign order ID and timestamp
            order_id = self._generate_order_id()
            timestamp = time.time()

            # Copy order to avoid mutating client input
            order = dict(incoming_order)
            order["order_id"] = order_id
            order["timestamp"] = timestamp

            # 3. Process order via order book
            trades, remaining_quantity = self._process_order(order)

            # 4. Emit execution / audit event
            self._emit_order_event(order, trades, remaining_quantity)

            # 5. Build success response
            return self._build_success_response(
                order_id=order_id,
                trades=trades,
                remaining_quantity=remaining_quantity
            )
        except Exception as e:
            # 6. Build standardized error response
                return self._build_error_response(
            incoming_order=incoming_order,
                error=str(e)
            )
        
        
    def _process_order(self, incoming_order: Dict) -> Tuple[List[Dict], int]:
        """
        Core order processing logic.

        Parameters:
            order (dict): validated order

        Returns:
            tuple:
                (
                    trades: List[dict],
                    remaining_quantity: int
                )
        """
        trades = []
        if incoming_order["order_type"] == "LIMIT":
            trades = self.order_book.process_limit_orders(Order.from_dict(incoming_order))
        else:
            trades = self.order_book.process_market_orders(Order.from_dict(incoming_order))
        remaining_quantity = incoming_order["quantity"]
        return (trades, remaining_quantity)

    def _validate_order(self, order: Dict) -> None:
        """
        Validate incoming order.

        Raises:
            ValueError: if order is invalid
        """
        
        required = {"user", "side", "quantity", "client_id", "order_type"}

        missing = required - order.keys()
        if missing:
            raise ValueError(f"Missing fields: {missing}")

        if order["side"] not in ("BUY", "SELL"):
            raise ValueError("Invalid side")

        if order["quantity"] <= 0:
            raise ValueError("Quantity must be positive")

        if order["order_type"] == "LIMIT" and "price" not in order:
            raise ValueError("LIMIT order requires price")


    def _assert_engine_running(self) -> None:
        """
        Ensure engine is in running state.
        """
        if not self._running:
            raise RuntimeError("Exchange engine is not running")

    def _generate_order_id(self) -> int:
        """
        Generate a unique order ID.

        Returns:
            int
        """
        return uuid.uuid4().int
        

    def _build_success_response(
        self,
        order_id: int,
        trades: List[Dict],
        remaining_quantity: int
    ) -> Dict:
        """
        Build a success response for client.
        """
        return {
            "accepted": True,
            "order_id": order_id,
            "trades": [t.to_dict() for t in trades],
            "remaining_quantity": remaining_quantity,
            "timestamp": time.time(),
            "message": self._execution_message(trades, remaining_quantity)
        }

    def _build_error_response(self, incoming_order: Dict, error: str) -> Dict:
        """
        Build standardized error response.
        """
        return {
            "accepted": False,
            "order_id": None,
            "trades": [],
            "remaining_quantity": incoming_order.get("quantity", 0),
            "timestamp": time.time(),
            "message": error
        }


    def _execution_message(
        self,
        trades: List[Dict],
        remaining_quantity: int
    ) -> str:
        """
        Generate execution message for client UI.
        """
        if not trades:
            return "Order accepted and placed in order book"

        if remaining_quantity == 0:
            return "Order fully executed"

        return "Order partially executed"

    def _emit_order_event(
        self,
        incoming_order: Dict,
        trades: List[Dict],
        remaining_quantity: int
    ) -> None:
        """
        Emit order/trade events for logging and persistence.
        """
        if not self.trade_writer:
            return

        for trade in trades:
            self.trade_writer.enqueue_trade(trade)


    def snapshot_state(self) -> Dict:
        """
        Return serializable snapshot of engine state.
        """
        return {
            "order_book": self.order_book.snapshot()
        }



    def restore_state(self, snapshot: Dict) -> None:
        """
        Restore engine state from snapshot.
        """
        self.order_book.restore(snapshot["order_book"])