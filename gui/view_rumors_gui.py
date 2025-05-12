import tkinter as tk
from tkinter import ttk
from models.rumor import Rumor
from models.character import Character
from models.faction import Faction
from models.location import Location
from utils.data_manager import load_data

DATA_FILE = "rumors.json"

def run_view_rumors_gui():
    window = tk.Toplevel()
    window.title("View Rumors")

    # Load reference data
    characters = {char.id: char.name for char in [Character.from_dict(c) for c in load_data("characters.json")]}
    factions = {fac.id: fac.name for fac in [Faction.from_dict(f) for f in load_data("factions.json")]}
    locations = {loc.id: loc.name for loc in [Location.from_dict(l) for l in load_data("locations.json")]}

    # Treeview setup
    columns = ("Content", "Source", "Date Heard", "Status", "Tags", "Characters", "Factions", "Location")
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(expand=True, fill="both")

    # Load rumors
    rumors = [Rumor.from_dict(d) for d in load_data(DATA_FILE)]
    for rumor in rumors:
        char_names = [characters.get(cid, f"Unknown ({cid})") for cid in rumor.related_characters]
        faction_names = [factions.get(fid, f"Unknown ({fid})") for fid in rumor.related_factions]
        location_name = locations.get(rumor.location_id, f"Unknown ({rumor.location_id})")
        
        tree.insert("", "end", values=(
            rumor.content,
            rumor.source,
            rumor.date_heard,
            rumor.status,
            ", ".join(rumor.tags),
            ", ".join(char_names),
            ", ".join(faction_names),
            location_name
        ))
