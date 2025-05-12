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
        description = entry_description.get("1.0", "end-1c")  # Get multi-line text from the description field
        connections = entry_connections.get()  # Get single-line text for connections
        
        # Load existing characters and generate a new ID for the new character
        characters = [Character.from_dict(c) for c in load_data(DATA_FILE)]
        new_id = len(characters) + 1  # Assign the next available ID
        
        # Split the connections into a list and create a new character object
        new_character = Character(
            id=new_id,  # Set the newly generated ID
            name=name,
            description=description,
            connections=connections.split(",")  # Convert comma-separated connections into a list
        )

        # Add the new character to the existing list and save to file
        characters.append(new_character)
        save_data(DATA_FILE, [char.to_dict() for char in characters])

        # Close the window after saving the character
        window.destroy()

    # UI Elements for the character form
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

    # Save Button to trigger saving the character
    button_save = ttk.Button(window, text="Save Character", command=save_character)
    button_save.pack(pady=10)

    # Run the GUI event loop to display the window
    window.mainloop()
