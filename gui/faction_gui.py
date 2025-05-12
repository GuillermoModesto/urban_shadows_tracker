import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data, save_data

DATA_FILE = "factions.json"

def run_faction_gui():
    window = tk.Toplevel()
    window.title("Add Faction")

    def save_faction():
        # Collect data from input fields
        name = entry_name.get()
        influence = entry_influence.get()
        territory = entry_territory.get()
        members = entry_members.get()

        # Generate a new ID
        factions = [Faction.from_dict(f) for f in load_data(DATA_FILE)]
        new_id = max((f.id for f in factions), default=0) + 1

        # Create new faction
        new_faction = Faction(
            id=new_id,
            name=name,
            influence=influence,
            territory=territory,
            members=[m.strip() for m in members.split(",")]
        )
        factions.append(new_faction)

        # Save to file
        save_data(DATA_FILE, [f.to_dict() for f in factions])
        window.destroy()

    # UI Layout
    tk.Label(window, text="Faction Name:").pack(pady=5)
    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    tk.Label(window, text="Influence:").pack(pady=5)
    entry_influence = tk.Entry(window)
    entry_influence.pack(pady=5)

    tk.Label(window, text="Territory:").pack(pady=5)
    entry_territory = tk.Entry(window)
    entry_territory.pack(pady=5)

    tk.Label(window, text="Members (comma separated):").pack(pady=5)
    entry_members = tk.Entry(window)
    entry_members.pack(pady=5)

    ttk.Button(window, text="Save Faction", command=save_faction).pack(pady=10)

    window.mainloop()
