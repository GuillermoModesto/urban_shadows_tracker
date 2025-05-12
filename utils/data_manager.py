import json
import os
import sys
import shutil

def resource_path(relative_path):
    """ Get absolute path to bundled resource (works for dev and PyInstaller) """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Path to external writable data directory
USER_DATA_DIR = os.path.join(os.getcwd(), "user_data")

# Files to manage
DATA_FILES = ["characters.json", "debts.json", "factions.json", "locations.json", "rumors.json"]

def ensure_user_data_exists():
    """ Ensure writable copies of bundled data exist in user_data/ """
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    for file in DATA_FILES:
        dest_path = os.path.join(USER_DATA_DIR, file)
        if not os.path.exists(dest_path):
            # Copy default file from bundled 'data' folder to user_data
            bundled_path = resource_path(os.path.join("data", file))
            if os.path.exists(bundled_path):
                shutil.copy(bundled_path, dest_path)
            else:
                # Create empty file if no default exists
                with open(dest_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

def load_data(filename, default_obj=None):
    path = os.path.join(USER_DATA_DIR, filename)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump([default_obj.to_dict()] if default_obj else [], f, indent=4)

    if os.stat(path).st_size == 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([default_obj.to_dict()] if default_obj else [], f, indent=4)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {filename} contains invalid JSON. Resetting file.")
        with open(path, "w", encoding="utf-8") as f:
            json.dump([default_obj.to_dict()] if default_obj else [], f, indent=4)
        return []

def save_data(filename, data):
    path = os.path.join(USER_DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
