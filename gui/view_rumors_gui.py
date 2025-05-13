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
    Runs the GUI for viewing rumors with filterable columns.
    """
    window = tk.Toplevel()
    window.title("View Rumors")

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), padding=5)
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11), rowheight=30)

    # Load related data
    characters = {char.id: char.name for char in [Character.from_dict(c) for c in load_data("characters.json")]}
    factions = {fac.id: fac.name for fac in [Faction.from_dict(f) for f in load_data("factions.json")]}
    locations = {loc.id: loc.name for loc in [Location.from_dict(l) for l in load_data("locations.json")]}
    rumors = [Rumor.from_dict(d) for d in load_data(DATA_FILE)]

    columns = ("Content", "Source", "Date Heard", "Status", "Tags", "Related Characters", "Related Factions", "Related Locations")

    # Filter bar
    filter_frame = tk.Frame(window)
    filter_frame.pack(fill="x", padx=5, pady=5)

    filter_vars = {col: tk.StringVar() for col in columns}
    for col in columns:
        col_frame = tk.Frame(filter_frame)
        col_frame.pack(side="left", expand=True, fill="x", padx=2)

        tk.Label(col_frame, text=col).pack(anchor="w")
        entry = tk.Entry(col_frame, textvariable=filter_vars[col])
        entry.pack(fill="x")
        entry.bind("<KeyRelease>", lambda e: update_tree())

    # Treeview
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    def format_rumor(rumor):
        return (
            rumor.content,
            rumor.source,
            rumor.date_heard,
            rumor.status,
            ", ".join(rumor.tags),
            ", ".join(characters.get(cid, str(cid)) for cid in rumor.related_characters),
            ", ".join(factions.get(fid, str(fid)) for fid in rumor.related_factions),
            ", ".join(locations.get(lid, str(lid)) for lid in rumor.related_locations)
        )

    def update_tree():
        tree.delete(*tree.get_children())
        for rumor in rumors:
            values = format_rumor(rumor)
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values)

    update_tree()
    window.mainloop()
