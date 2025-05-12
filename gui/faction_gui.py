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
        name = entry_name.get()
        description = entry_description.get("1.0", "end-1c")  # Text widget
        territory = entry_territory.get()
        members = entry_members.get()

        # Automatically generate the ID based on current data
        factions = load_data(DATA_FILE)
        new_id = len(factions) + 1  # Next available ID

        # Create a new faction and save it
        new_faction = Faction(
            id=new_id,  # Automatically generated ID
            name=name,
            description=description,
            territory=territory,
            members=members.split(",")  # Split members by commas
        )
        factions.append(new_faction)
        save_data(DATA_FILE, [f.to_dict() for f in factions])

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

    button_save = ttk.Button(window, text="Save Faction", command=save_faction)
    button_save.pack(pady=10)

    window.mainloop()
