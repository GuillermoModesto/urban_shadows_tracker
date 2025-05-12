import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data

DATA_FILE = "locations.json"

def run_view_locations_gui():
    """
    GUI for viewing locations with filterable columns.
    """
    window = tk.Toplevel()
    window.title("View Locations")

    columns = ("Name", "Description", "Area", "Details")
    locations = [Location.from_dict(d) for d in load_data(DATA_FILE)]

    # Filter inputs frame
    filter_frame = tk.Frame(window)
    filter_frame.pack(fill="x", padx=5, pady=5)

    filter_vars = {col: tk.StringVar() for col in columns}

    for col in columns:
        sub_frame = tk.Frame(filter_frame)
        sub_frame.pack(side="left", expand=True, fill="x", padx=2)

        label = tk.Label(sub_frame, text=col)
        label.pack(anchor="w")

        entry = tk.Entry(sub_frame, textvariable=filter_vars[col])
        entry.pack(fill="x")
        entry.bind("<KeyRelease>", lambda e: update_tree())

    # Treeview setup
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    def update_tree():
        tree.delete(*tree.get_children())
        for loc in locations:
            values = (
                loc.name,
                loc.description,
                loc.area,
                ", ".join(loc.details) if isinstance(loc.details, list) else loc.details
            )
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values)

    update_tree()  # Show all on startup

    window.mainloop()
