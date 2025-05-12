import tkinter as tk
from tkinter import ttk
from models.rumor import Rumor
from models.character import Character
from models.faction import Faction
from models.location import Location
from utils.data_manager import load_data

DATA_FILE = "rumors.json"

def run_view_rumors_gui():
    """
    Runs the GUI for viewing rumors. Displays a table with rumor details including content, source, status, 
    related characters, factions, and locations.
    """
    # Create a new window for viewing rumors
    window = tk.Toplevel()
    window.title("View Rumors")

    # Load reference data for characters, factions, and locations
    # Create dictionaries mapping IDs to names for easy lookup
    characters = {char.id: char.name for char in [Character.from_dict(c) for c in load_data("characters.json")]}
    factions = {fac.id: fac.name for fac in [Faction.from_dict(f) for f in load_data("factions.json")]}
    locations = {loc.id: loc.name for loc in [Location.from_dict(l) for l in load_data("locations.json")]}

    # Set up the Treeview widget with columns for rumor details
    columns = ("Content", "Source", "Date Heard", "Status", "Tags", "Characters", "Factions", "Related Locations")
    tree = ttk.Treeview(window, columns=columns, show='headings')
    
    # Configure the columns and their headers
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)  # Set the width for each column
    
    # Pack the Treeview widget into the window
    tree.pack(expand=True, fill="both")

    # Load the list of rumors from the data file and convert them to Rumor objects
    rumors = [Rumor.from_dict(d) for d in load_data(DATA_FILE)]
    
    # Insert each rumor into the Treeview
    for rumor in rumors:
        # Get the names for the related characters, factions, and locations
        char_names = [characters.get(cid, f"{cid}") for cid in rumor.related_characters]
        faction_names = [factions.get(fid, f"{fid}") for fid in rumor.related_factions]
        location_names = [locations.get(lid, f"{lid}") for lid in rumor.related_locations]

        # Insert the rumor data into the treeview
        tree.insert("", "end", values=(
            rumor.content,  # Rumor content
            rumor.source,  # Source of the rumor
            rumor.date_heard,  # Date when the rumor was heard
            rumor.status,  # Status of the rumor (e.g., unconfirmed, confirmed)
            ", ".join(rumor.tags),  # Tags associated with the rumor
            ", ".join(char_names),  # Related characters' names
            ", ".join(faction_names),  # Related factions' names
            ", ".join(location_names)  # Related locations' names
        ))

    # Start the Tkinter event loop
    window.mainloop()
