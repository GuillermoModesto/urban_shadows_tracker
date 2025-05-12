import tkinter as tk
from tkinter import ttk
from models.character import Character
from utils.data_manager import load_data

DATA_FILE = "characters.json"

def run_view_characters_gui():
    window = tk.Toplevel()
    window.title("View Characters")

    # Treeview for displaying characters
    tree = ttk.Treeview(window, columns=("ID", "Name", "Description", "Connections"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill="both")

    # Load characters from the data file
    characters = [Character.from_dict(d) for d in load_data(DATA_FILE)]
    for character in characters:
        tree.insert("", "end", values=(
            character.id, character.name, character.description, ", ".join(character.connections)
        ))

    window.mainloop()
