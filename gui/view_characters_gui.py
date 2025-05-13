import tkinter as tk
from tkinter import ttk
from models.character import Character
from utils.data_manager import load_data
from utils.style import apply_treeview_styles

DATA_FILE = "characters.json"

def run_view_characters_gui():
    """
    GUI for viewing characters with column-specific filters.
    """
    window = tk.Toplevel()
    window.title("View Characters")

    apply_treeview_styles()

    columns = ("Name", "Description", "Faction", "Group", "Connections")
    characters = [Character.from_dict(d) for d in load_data(DATA_FILE)]

    # Frame for filters
    filter_frame = tk.Frame(window)
    filter_frame.pack(fill="x", padx=5, pady=5)

    # StringVars for filters
    filter_vars = {col: tk.StringVar() for col in columns}

    # Create filter inputs with labels
    for col in columns:
        sub_frame = tk.Frame(filter_frame)
        sub_frame.pack(side="left", expand=True, fill="x", padx=2)

        label = tk.Label(sub_frame, text=col)
        label.pack(anchor="w")

        entry = tk.Entry(sub_frame, textvariable=filter_vars[col])
        entry.pack(fill="x")
        entry.bind("<KeyRelease>", lambda e: update_tree())

    # Treeview setup
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    def update_tree():
        tree.delete(*tree.get_children())
        for char in characters:
            values = (char.name, char.description, char.from_faction, char.from_group, ", ".join(char.connections))
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values)

    update_tree()  # Show all characters by default

    window.mainloop()
