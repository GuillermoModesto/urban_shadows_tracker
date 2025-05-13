import json
import os
import sys
import shutil

def resource_path(relative_path):
    """
    Get absolute path to a bundled resource, which works both in development 
    and when bundled with PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller stores resources here
    except AttributeError:
        base_path = os.path.abspath(".")  # Default location in dev mode
    return os.path.join(base_path, relative_path)

# Path to the external writable data directory
USER_DATA_DIR = os.path.join(os.getcwd(), "data")

# List of data files to manage
DATA_FILES = ["characters.json", "debts.json", "factions.json", "locations.json", "rumors.json"]

def ensure_user_data_exists():
    """
    Ensure that writable copies of bundled data files exist in the user data directory.
    If the files don't exist, copy them from the bundled resources or create empty files.

    Creates the 'data' directory if it does not already exist.
    """
    os.makedirs(USER_DATA_DIR, exist_ok=True)

    for file in DATA_FILES:
        dest_path = os.path.join(USER_DATA_DIR, file)
        if not os.path.exists(dest_path):
            # Copy the file from bundled resources if it exists
            bundled_path = resource_path(os.path.join("data", file))
            if os.path.exists(bundled_path):
                shutil.copy(bundled_path, dest_path)
            else:
                # If no bundled file exists, create an empty file
                with open(dest_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)

def load_data(filename, default_obj=None):
    """
    Load data from a JSON file. If the file doesn't exist or is empty, it creates
    a new file with default data.

    Args:
        filename (str): The name of the file to load data from.
        default_obj (optional): An object to use as the default data (if file is empty or doesn't exist).

    Returns:
        list: The data loaded from the file, or an empty list if no data exists.
    """
    path = os.path.join(USER_DATA_DIR, filename)

    # Ensure the file exists and is not empty
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([default_obj.to_dict()] if default_obj else [], f, indent=4)

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {filename} contains invalid JSON. Resetting file.")
        # If the file is corrupted, reset it to default data
        with open(path, "w", encoding="utf-8") as f:
            json.dump([default_obj.to_dict()] if default_obj else [], f, indent=4)
        return []

def save_data(filename, data):
    """
    Save the provided data to a JSON file.

    Args:
        filename (str): The name of the file to save data to.
        data (list): The data to save to the file.
    """
    path = os.path.join(USER_DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
