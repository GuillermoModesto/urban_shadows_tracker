import tkinter as tk
from tkinter import ttk
from models.character import Character
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles
from models.faction import Faction

DATA_FILE = "characters.json"
FACTIONS_FILE = "factions.json"

def run_character_gui():
    """
    Creates and displays a GUI for adding a new character, 
    with fields for character name, description, faction, group, and connections.
    """
    window = tk.Toplevel()
    window.title("Add Character")

    apply_global_styles()

    # Load all factions from the data file and create a list of their names
    factions = [Faction.from_dict(f) for f in load_data(FACTIONS_FILE)]
    faction_names = [faction.name for faction in factions]

    def save_character():
        """
        Collects the data from the input fields, creates a new Character object,
        and saves the character to the data file.
        """
        name = entry_name.get()
        description = entry_description.get("1.0", "end-1c")
        connections = entry_connections.get()
        from_faction = combo_faction.get()
        from_group = entry_from_group.get()

        # Load existing characters and assign a new ID
        characters = [Character.from_dict(c) for c in load_data(DATA_FILE)]
        new_id = len(characters) + 1

        # Split the connections into a list and create a new character
        new_character = Character(
            id=new_id,
            name=name,
            description=description,
            from_faction=from_faction,
            from_group=from_group,
            connections=connections.split(",")
        )

        # Save the new character to the file
        characters.append(new_character)
        save_data(DATA_FILE, [char.to_dict() for char in characters])

        # Close the character creation window
        window.destroy()

    # Character name input
    label_name = ttk.Label(window, text="Character Name:")
    label_name.pack(pady=5)
    entry_name = ttk.Entry(window)
    entry_name.pack(pady=5)

    # Character description input
    label_description = ttk.Label(window, text="Character Description:")
    label_description.pack(pady=5)
    entry_description = tk.Text(window, height=4, width=20)
    entry_description.pack(pady=5)

    # Faction selection combobox
    label_from_faction = ttk.Label(window, text="From Faction:")
    label_from_faction.pack(pady=5)
    combo_faction = ttk.Combobox(window, values=faction_names, state="normal")
    combo_faction.pack(pady=5)

    # Group input
    label_from_group = ttk.Label(window, text="From Group:")
    label_from_group.pack(pady=5)
    entry_from_group = ttk.Entry(window)
    entry_from_group.pack(pady=5)

    # Connections input
    label_connections = ttk.Label(window, text="Connections (comma separated):")
    label_connections.pack(pady=5)
    entry_connections = ttk.Entry(window)
    entry_connections.pack(pady=5)

    # Save button to save the new character
    button_save = ttk.Button(window, text="Save Character", command=save_character)
    button_save.pack(pady=10)

    # Start the GUI event loop
    window.mainloop()
