import threading
import queue
import time

from utils.file_io import *
from utils.serialization import *
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
        #if already running the thread
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._writer_loop,
            name="TradeWriterThread",
            daemon=True
        )
        self._thread.start()

    def enqueue_trade(self, trade: Trade):
        """
        Submit a trade for asynchronous persistence.

        This method MUST be non-blocking.
        """
        if not self._running:
            raise RuntimeError("TradeWriter Thread is not running")

        self._queue.put(trade)


    def _writer_loop(self):
        """
        Background worker loop.

        Consumes trades in FIFO order and appends them to the ledger.
        """
        while self._running or not self._queue.empty(): 

            try: 
                trade = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            try: 
                # serialize the data 
                record = trade.to_dict()
                #append this to the trade.json
                self.append_trade(record)
            finally:
                self._queue.task_done()

                
                

    def flush(self):
        """
        Flush all pending trades to disk.
        """
        self._queue.join()

    def stop(self):
        """
        Stop the background writer gracefully.
        """
        if not self._running:
            return
        
        self._running = False
        self.flush()

        if self._thread:
            self._thread.join()
            self._thread = None

    def is_running(self) -> bool:
        """
        Check whether the trade writer is currently active.
        """
        return self._running

    def append_trade(self, trade: dict):
        """
        Append a trade record to storage/trades/trades.json
        """
        from utils.file_io import ensure_dir
        ensure_dir("storage/trades")
        append_json(self.ledger_path, trade)
