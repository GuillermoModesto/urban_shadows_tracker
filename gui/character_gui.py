import tkinter as tk
from tkinter import ttk
from models.character import Character
from utils.data_manager import load_data, save_data

DATA_FILE = "characters.json"

def run_character_gui():
    window = tk.Toplevel()
    window.title("Add Character")

    def save_character():
        # Collect data from the input fields
        name = entry_name.get()
        description = entry_description.get("1.0", "end-1c")  # Text widget (multi-line)
        connections = entry_connections.get()  # Single-line entry field for connections
        
        # Automatically generate the ID based on current data
        characters = [Character.from_dict(c) for c in load_data(DATA_FILE)]
        new_id = len(characters) + 1  # Next available ID
        
        # Split connections by commas and create the new character object
        new_character = Character(
            id=new_id,  # Automatically generated ID
            name=name,
            description=description,
            connections=connections.split(",")  # Split connections by commas
        )

        # Append the new character to the list and save
        characters.append(new_character)
        save_data(DATA_FILE, [char.to_dict() for char in characters])

        # Close the window after saving
        window.destroy()

    # UI Elements
    label_name = tk.Label(window, text="Character Name:")
    label_name.pack(pady=5)
    entry_name = tk.Entry(window)
    entry_name.pack(pady=5)

    label_description = tk.Label(window, text="Character Description:")
    label_description.pack(pady=5)
    entry_description = tk.Text(window, height=5, width=40)
    entry_description.pack(pady=5)

    label_connections = tk.Label(window, text="Connections (comma separated):")
    label_connections.pack(pady=5)
    entry_connections = tk.Entry(window)
    entry_connections.pack(pady=5)

    # Save Button
    button_save = ttk.Button(window, text="Save Character", command=save_character)
    button_save.pack(pady=10)

    # Run the GUI event loop
    window.mainloop()
