import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "factions.json"

def run_faction_gui():
    """
    Creates and displays a GUI for adding a new faction, 
    allowing input of name, influence, territory, and members.
    """
    window = tk.Toplevel()
    window.title("Add Faction")

    apply_global_styles()

    def save_faction():
        """
        Collects form data, creates a new Faction object,
        and saves it to the data file.
        """
        name = entry_name.get()
        influence = entry_influence.get()
        territory = entry_territory.get()
        members = entry_members.get()

        # Load existing factions and compute next available ID
        factions = [Faction.from_dict(f) for f in load_data(DATA_FILE)]
        new_id = max((f.id for f in factions), default=0) + 1

        # Create new faction instance
        new_faction = Faction(
            id=new_id,
            name=name,
            influence=influence,
            territory=territory,
            members=[m.strip() for m in members.split(",")]
        )
        factions.append(new_faction)

        # Save updated faction list
        save_data(DATA_FILE, [f.to_dict() for f in factions])
        window.destroy()

    # Faction name input
    ttk.Label(window, text="Faction Name:").pack(pady=5)
    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    # Influence input
    ttk.Label(window, text="Influence:").pack(pady=5)
    entry_influence = tk.Entry(window)
    entry_influence.pack(pady=5)

    # Territory input
    ttk.Label(window, text="Territory:").pack(pady=5)
    entry_territory = tk.Entry(window)
    entry_territory.pack(pady=5)

    # Members input (comma-separated)
    ttk.Label(window, text="Members (comma separated):").pack(pady=5)
    entry_members = tk.Entry(window)
    entry_members.pack(pady=5)

    # Save button
    ttk.Button(window, text="Save Faction", command=save_faction).pack(pady=10)

    # Display the window
    window.mainloop()
