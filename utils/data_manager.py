import json
import os

def load_data(filename, default_obj=None):
    path = os.path.join("data", filename)

    # Create file if it doesn't exist
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            if default_obj:
                json.dump([default_obj.to_dict()], f, indent=4)
            else:
                json.dump([], f, indent=4)

    # Handle empty file
    if os.stat(path).st_size == 0:
        with open(path, "w", encoding="utf-8") as f:
            if default_obj:
                json.dump([default_obj.to_dict()], f, indent=4)
            else:
                json.dump([], f, indent=4)

    # Try to load the JSON data
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {filename} contains invalid JSON. Resetting file.")
            with open(path, "w", encoding="utf-8") as f_reset:
                if default_obj:
                    json.dump([default_obj.to_dict()], f_reset, indent=4)
                else:
                    json.dump([], f_reset, indent=4)
            return []


def save_data(filename, data):
    path = os.path.join("data", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)