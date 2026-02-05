import threading
import queue
import time

from utils.file_io import FileIO
from utils.serialization import SerializationUtils
from engine.trade import Trade


class TradeWriter:
    """
    Asynchronous trade persistence manager.

    The TradeWriter acts as a background worker that:
    - Receives executed Trade objects from the engine
    - Queues them for persistence
    - Writes them to the trade ledger in FIFO order

    This class follows a producer-consumer model:
    - Engine = producer
    - TradeWriter = consumer
    """

    def __init__(self, ledger_path: str):
        """
        Initialize the trade writer.
        """
        self.ledger_path = ledger_path
        self._queue = queue.Queue()
        self._thread = None
        self._running = False

    def start(self):
        """
        Start the background trade writing process.
        """
        pass

    def enqueue_trade(self, trade: Trade):
        """
        Submit a trade for asynchronous persistence.

        This method MUST be non-blocking.
        """
        pass

    def _writer_loop(self):
        """
        Background worker loop.

        Consumes trades in FIFO order and appends them to the ledger.
        """
        pass

    def flush(self):
        """
        Flush all pending trades to disk.
        """
        pass

    def stop(self):
        """
        Stop the background writer gracefully.
        """
        pass

    def is_running(self) -> bool:
        """
        Check whether the trade writer is currently active.
        """
        pass