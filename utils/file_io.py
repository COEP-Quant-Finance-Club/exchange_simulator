class FileIO:
    """
    Low-level file operations.

    Responsible only for:
    - Reading files
    - Writing files
    - Creating directories if missing
    """

    @staticmethod
    def read_text(path: str) -> str:
        """
        Read entire file content as string.
        """

    @staticmethod
    def write_text(path: str, content: str):
        """
        Write string content to file.
        Overwrites existing content.
        """

    @staticmethod
    def append_text(path: str, content: str):
        """
        Append string content to file.
        """

    @staticmethod
    def ensure_dir(path: str):
        """
        Create directory if it does not exist.
        """
