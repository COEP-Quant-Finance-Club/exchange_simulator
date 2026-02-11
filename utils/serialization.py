import json
import os

def log_info(message):
    """
    Logs informational message to system log file
    """

def load_json(path):
    """
    Loads JSON file and returns list.
    Returns empty list if file does not exist.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def save_json(path, data):
    """
    Saves data to JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def append_json(path, record):
    """
    Appends a record to JSON list file.
    """
    data = load_json(path)
    data.append(record)
    save_json(path, data)

