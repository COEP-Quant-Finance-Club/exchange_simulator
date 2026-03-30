import os

def ensure_dir(path):
    """
    Create directory if it does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def ensure_file(path):
    """
    Create empty file if it does not exist.
    """
    directory = os.path.dirname(path)
    if directory:
        ensure_dir(directory)

    if not os.path.exists(path):
        open(path, "w").close()
