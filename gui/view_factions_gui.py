import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data

DATA_FILE = "factions.json"

def run_view_factions_gui():
    """
    Runs the GUI for viewing factions. Displays a table with faction details including ID, name, influence, territory, and members.
    """
    # Create a new window for viewing factions
    window = tk.Toplevel()
    window.title("View Factions")

    # Set up the Treeview widget to display faction data
    tree = ttk.Treeview(window, columns=("Name", "Influence", "Territory", "Members"), show="headings")
    
    # Configure the columns for the Treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Set the heading for each column
        tree.column(col, width=120)  # Set the width for each column
        
    tree.pack(expand=True, fill="both")  # Pack the Treeview widget into the window

    # Load the list of factions from the data file and convert to Faction objects
    factions = [Faction.from_dict(d) for d in load_data(DATA_FILE)]  # Load data and convert to Faction objects

    # Insert each faction into the Treeview
    for faction in factions:
        tree.insert("", "end", values=(
            faction.name,  # Faction name
            faction.influence,  # Faction's influence
            faction.territory,  # Faction's territory
            ", ".join(faction.members)  # Faction members, assuming it's a list of names
        ))

    # Start the Tkinter event loop
    window.mainloop()
