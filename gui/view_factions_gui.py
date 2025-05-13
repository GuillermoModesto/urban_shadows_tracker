import tkinter as tk
from tkinter import ttk
from models.faction import Faction
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "factions.json"


def run_view_factions_gui():
    """
    Launches a GUI for viewing and editing factions.
    Features:
    - Filterable columns
    - In-cell editing via double-click
    """
    window = tk.Toplevel()
    window.title("View Factions")
    apply_global_styles()

    columns = ("Name", "Influence", "Territory", "Members")
    factions = [Faction.from_dict(d) for d in load_data(DATA_FILE)]

    # Filter controls
    filter_frame = tk.Frame(window)
    filter_frame.pack(fill="x", padx=5, pady=5)

    filter_vars = {col: tk.StringVar() for col in columns}
    for col in columns:
        sub_frame = tk.Frame(filter_frame)
        sub_frame.pack(side="left", expand=True, fill="x", padx=2)

        tk.Label(sub_frame, text=col).pack(anchor="w")
        entry = tk.Entry(sub_frame, textvariable=filter_vars[col])
        entry.pack(fill="x")
        entry.bind("<KeyRelease>", lambda e: update_tree())

    # Table
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    # Editing state
    edit_window = None
    edit_var = tk.StringVar()
    current_item = None
    current_column = None

    def update_tree():
        """Refreshes the treeview based on filters."""
        tree.delete(*tree.get_children())
        for faction in factions:
            values = (
                faction.name,
                faction.influence,
                faction.territory,
                ", ".join(faction.members),
            )
            if all(filter_vars[col].get().lower() in str(values[i]).lower()
                   for i, col in enumerate(columns)):
                tree.insert("", "end", values=values, iid=faction.name)

    def save_edit():
        """Saves the edited value and updates the file."""
        nonlocal edit_window, current_item, current_column

        new_value = edit_var.get()
        faction_name = tree.item(current_item)['values'][0]
        faction = next((f for f in factions if f.name == faction_name), None)

        if faction:
            if current_column == "Name":
                faction.name = new_value
            elif current_column == "Influence":
                faction.influence = new_value
            elif current_column == "Territory":
                faction.territory = new_value
            elif current_column == "Members":
                faction.members = [m.strip() for m in new_value.split(",")]

            save_data(DATA_FILE, [f.to_dict() for f in factions])
            update_tree()

        if edit_window:
            edit_window.destroy()
            edit_window = None

    def on_double_click(event):
        """Opens a pop-up editor on cell double-click."""
        nonlocal edit_window, current_item, current_column

        if tree.identify("region", event.x, event.y) != "cell":
            return

        current_item = tree.identify_row(event.y)
        col_index = int(tree.identify_column(event.x)[1:]) - 1
        current_column = columns[col_index]

        current_value = tree.item(current_item)["values"][col_index]
        edit_var.set(current_value)

        if edit_window:
            edit_window.destroy()

        edit_window = tk.Toplevel(window)
        edit_window.title(f"Edit {current_column}")
        x = window.winfo_x() + event.x + 50
        y = window.winfo_y() + event.y + 50
        edit_window.geometry(f"300x100+{x}+{y}")

        entry = tk.Entry(edit_window, textvariable=edit_var)
        entry.pack(fill="x", padx=5, pady=5)
        entry.bind("<Return>", lambda e: save_edit())
        entry.focus_set()
        entry.select_range(0, tk.END)

        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(button_frame, text="Save", command=save_edit).pack(side="right", padx=5)
        tk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="right", padx=5)

    tree.bind("<Double-1>", on_double_click)

    update_tree()
    window.mainloop()
