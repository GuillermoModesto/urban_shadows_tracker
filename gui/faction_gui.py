import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data, save_data

DATA_FILE = "factions.json"

def run_faction_gui():
    window = tk.Toplevel()
    window.title("Add Faction")

    def save_faction():
        # Collect data from the input fields
        name = entry_name.get()  # Get the faction name
        description = entry_description.get("1.0", "end-1c")  # Get the description (multi-line)
        territory = entry_territory.get()  # Get the territory
        members = entry_members.get()  # Get the members (comma separated)

        # Generate the new faction ID based on existing data
        factions = load_data(DATA_FILE)
        new_id = len(factions) + 1  # Automatically assign the next available ID

        # Create the new faction object and append it to the list
        new_faction = Faction(
            id=new_id,
            name=name,
            description=description,
            territory=territory,
            members=members.split(",")  # Split members by commas
        )
        factions.append(new_faction)

        # Save the updated list of factions to the file
        save_data(DATA_FILE, [f.to_dict() for f in factions])

        # Close the window after saving
        window.destroy()

    # UI Elements
    label_name = tk.Label(window, text="Faction Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    label_description = tk.Label(window, text="Faction Description:")
    label_description.pack(pady=5)
    entry_description = tk.Text(window, height=5, width=40)
    entry_description.pack(pady=5)

    label_territory = tk.Label(window, text="Territory:")
    label_territory.pack(pady=5)
    entry_territory = tk.Entry(window)
    entry_territory.pack(pady=5)

    label_members = tk.Label(window, text="Members (comma separated):")
    label_members.pack(pady=5)
    entry_members = tk.Entry(window)
    entry_members.pack(pady=5)

    # Button to save the new faction
    button_save = ttk.Button(window, text="Save Faction", command=save_faction)
    button_save.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()
