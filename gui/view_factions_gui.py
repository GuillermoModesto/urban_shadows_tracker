import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data

DATA_FILE = "factions.json"

def run_view_factions_gui():
    window = tk.Toplevel()
    window.title("View Factions")

    # Setup the Treeview widget
    tree = ttk.Treeview(window, columns=("ID", "Name", "Influence", "Territory", "Members"), show="headings")
    
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
        
    tree.pack(expand=True, fill="both")

    # Load data
    factions = [Faction.from_dict(d) for d in load_data(DATA_FILE)]

    # Insert data into the treeview
    for faction in factions:
        tree.insert("", "end", values=(
            faction.id,
            faction.name,
            faction.influence,
            faction.territory,
            ", ".join(faction.members)  # Assuming members is a list of names
        ))

    window.mainloop()
