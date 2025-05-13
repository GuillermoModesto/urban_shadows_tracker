import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data
from utils.style import apply_global_styles

DATA_FILE = "factions.json"

def run_view_factions_gui():
    """
    GUI for viewing factions with filterable columns.
    """
    window = tk.Toplevel()
    window.title("View Factions")

    apply_global_styles()

    columns = ("Name", "Influence", "Territory", "Members")
    factions = [Faction.from_dict(d) for d in load_data(DATA_FILE)]

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
        tree.column(col, width=140)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    def update_tree():
        tree.delete(*tree.get_children())
        for faction in factions:
            values = (
                faction.name,
                faction.influence,
                faction.territory,
                ", ".join(faction.members)
            )
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values)

    update_tree()  # Initial load with all entries

    window.mainloop()
