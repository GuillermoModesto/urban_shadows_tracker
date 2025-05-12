# gui/view_locations_gui.py
import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data

DATA_FILE = "locations.json"

def run_view_locations_gui():
    window = tk.Toplevel()
    window.title("View Locations")

    tree = ttk.Treeview(window, columns=("ID", "Name", "Description", "District"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(expand=True, fill="both")

    locations = [Location.from_dict(d) for d in load_data(DATA_FILE)]
    for loc in locations:
        tree.insert("", "end", values=(loc.id, loc.name, loc.description, loc.district))
