class SerializationUtils:
    """
    Handles conversion between:
    - Plain Python data (dict, list, int, str)
    - JSON strings

    This is a boundary utility.
    It must NEVER contain domain logic.
    """

    @staticmethod
    def to_json(data: dict) -> str:
        """
        Convert plain Python data into JSON string.

        Assumes data is already JSON-serializable.
        """

    @staticmethod
    def from_json(json_str: str) -> dict:
        """
        Convert JSON string into plain Python data.
        """
