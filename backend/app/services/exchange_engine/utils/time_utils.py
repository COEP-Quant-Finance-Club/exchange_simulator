from datetime import datetime
import time
def current_timestamp():
    """
    Returns current time as string in YYYY-MM-DD HH:MM:SS format
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_timestamp():
    return datetime.now()

def get_formated_timestamp(timestamp):
    """Returns an formated timestamp"""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
