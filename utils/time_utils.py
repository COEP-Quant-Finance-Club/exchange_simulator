from datetime import datetime

def current_timestamp():
    """
    Returns current time as string in YYYY-MM-DD HH:MM:SS format
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
