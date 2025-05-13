import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "locations.json"

def run_location_gui():
    """
    Launches a GUI window for adding a new location. 
    Users can input a name, description, area, and a list of details.
    """
    window = tk.Toplevel()
    window.title("Add Location")

    apply_global_styles()

    def save_location():
        """
        Collects input values, creates a new Location object,
        appends it to the data list, and saves it to file.
        """
        name = entry_name.get()
        description = entry_description.get("1.0", "end-1c")
        area = entry_area.get()
        details = entry_details.get()

        locations_data = load_data(DATA_FILE)
        locations = [Location.from_dict(loc_data) for loc_data in locations_data]
        new_id = len(locations) + 1

        new_location = Location(
            id=new_id,
            name=name,
            description=description,
            area=area,
            details=[d.strip() for d in details.split(",")]
        )
        locations.append(new_location)

        save_data(DATA_FILE, [l.to_dict() for l in locations])
        window.destroy()

    # Location Name
    ttk.Label(window, text="Location Name:").pack(pady=5)
    entry_name = ttk.Entry(window)
    entry_name.pack(pady=5)

    # Description (multiline)
    ttk.Label(window, text="Location Description:").pack(pady=5)
    entry_description = tk.Text(window, height=4, width=20)
    entry_description.pack(pady=5)

    # Area
    ttk.Label(window, text="Area:").pack(pady=5)
    entry_area = ttk.Entry(window)
    entry_area.pack(pady=5)

    # Details (comma-separated)
    ttk.Label(window, text="Details (comma separated):").pack(pady=5)
    entry_details = ttk.Entry(window)
    entry_details.pack(pady=5)

    # Save Button
    ttk.Button(window, text="Save Location", command=save_location).pack(pady=10)

    window.mainloop()
