import json
import os
from datetime import datetime

def log_info(message):
    """
    Logs informational message to system log file
    """
    print(message)
    

def load_json(path):
    
    if not os.path.exists(path):
        return []

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_json(path, data):
    """
    Saves data to JSON file.
    Automatically converts datetime objects to ISO strings.
    """
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(path, "w") as f:
        json.dump(data, f, indent=4, default=default_serializer)

def append_json(path, record):
    """
    Appends a record to JSON list file.
    """
    data = load_json(path)
    data.append(record)
    save_json(path, data)

