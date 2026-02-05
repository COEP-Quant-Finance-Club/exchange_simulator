class Logger:
    """
    User-specific audit logger.

    Used to record:
    - Order placement
    - Trade execution
    - System events

    Logs are human-readable and append-only.
    """

    def __init__(self, user: str):
        """
        Initialize logger for a specific user.
        """

    def log_order_placed(self, message: str):
        """
        Log order placement event.
        """

    def log_trade_executed(self, message: str):
        """
        Log trade execution event.
        """

    def log_system(self, message: str):
        """
        Log generic system messages.
        """
