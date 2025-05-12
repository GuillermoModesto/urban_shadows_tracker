import tkinter as tk
from tkinter import ttk
from models.character import Character
from utils.data_manager import load_data

DATA_FILE = "characters.json"

def run_view_characters_gui():
    """
    Runs the GUI for viewing characters. Displays a table of all characters and their details.
    """
    # Create a new window for viewing characters
    window = tk.Toplevel()
    window.title("View Characters")

    # Set up the Treeview widget to display character data
    tree = ttk.Treeview(window, columns=("Name", "Description", "Connections"), show='headings')
    
    # Configure the columns for the Treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Set the heading for each column
        tree.column(col, width=120)  # Set the width for each column
    tree.pack(expand=True, fill="both")  # Pack the Treeview widget into the window

    # Load the list of characters from the data file
    characters = [Character.from_dict(d) for d in load_data(DATA_FILE)]  # Convert loaded data into Character objects
    
    # Insert each character into the Treeview
    for character in characters:
        tree.insert("", "end", values=(
            character.name,  # Name of the character
            character.description,  # Description of the character
            ", ".join(character.connections)  # List of connections joined by commas
        ))

    # Start the Tkinter event loop
    window.mainloop()
