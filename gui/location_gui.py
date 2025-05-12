import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data, save_data

DATA_FILE = "locations.json"

def run_location_gui():
    window = tk.Toplevel()
    window.title("Add Location")

    def save_location():
        # Collect data from the input fields
        name = entry_name.get()  # Get the location name
        description = entry_description.get("1.0", "end-1c")  # Get the description (multi-line)
        area = entry_area.get()  # Get the area
        details = entry_details.get()  # Get the details (comma separated)

        # Generate the new location ID based on existing data
        locations_data = load_data(DATA_FILE)
        locations = [Location.from_dict(loc_data) for loc_data in locations_data]
        new_id = len(locations) + 1  # Automatically assign the next available ID

        # Create the new location object and append it to the list
        new_location = Location(
            id=new_id,
            name=name,
            description=description,
            area=area,
            details=details.split(",")  # Split details by commas
        )
        locations.append(new_location)

        # Save the updated list of locations to the file
        save_data(DATA_FILE, [l.to_dict() for l in locations])

        # Close the window after saving
        window.destroy()

    # UI Elements
    label_name = tk.Label(window, text="Location Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    label_description = tk.Label(window, text="Location Description:")
    label_description.pack(pady=5)
    entry_description = tk.Text(window, height=5, width=40)
    entry_description.pack(pady=5)

    label_area = tk.Label(window, text="Area:")
    label_area.pack(pady=5)
    entry_area = tk.Entry(window)
    entry_area.pack(pady=5)

    label_details = tk.Label(window, text="Details (comma separated):")
    label_details.pack(pady=5)
    entry_details = tk.Entry(window)
    entry_details.pack(pady=5)

    # Button to save the new location
    button_save = ttk.Button(window, text="Save Location", command=save_location)
    button_save.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()
