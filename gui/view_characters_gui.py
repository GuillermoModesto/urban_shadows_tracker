import tkinter as tk
from tkinter import ttk
from models.character import Character
from models.faction import Faction
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "characters.json"
FACTIONS_FILE = "factions.json"


def run_view_characters_gui():
    """
    Launches a GUI to view and edit characters.
    Features:
    - Filterable columns
    - In-cell editing
    - Faction editing via dropdown using known faction names
    """
    window = tk.Toplevel()
    window.title("View Characters")
    apply_global_styles()

    # Load data
    factions = [Faction.from_dict(f) for f in load_data(FACTIONS_FILE)]
    faction_names = [f.name for f in factions]
    characters = [Character.from_dict(c) for c in load_data(DATA_FILE)]

    columns = ("Name", "Description", "Faction", "Group", "Connections")

    # Filter UI
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
        tree.column(col, width=150)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    # Edit state
    edit_window = None
    edit_var = tk.StringVar()
    current_item = None
    current_column = None

    def update_tree():
        """Refreshes the treeview based on filters."""
        tree.delete(*tree.get_children())
        for char in characters:
            values = (
                char.name,
                char.description,
                char.from_faction,
                char.from_group,
                ", ".join(char.connections)
            )
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values)

    def save_edit():
        """Saves the edited value back to the character and updates file."""
        nonlocal edit_window, current_item, current_column

        if current_column == "Faction":
            new_value = faction_combobox.get()
        else:
            new_value = edit_var.get()

        char_name = tree.item(current_item)['values'][0]
        character = next((c for c in characters if c.name == char_name), None)

        if character:
            if current_column == "Name":
                character.name = new_value
            elif current_column == "Description":
                character.description = new_value
            elif current_column == "Faction":
                character.from_faction = new_value
            elif current_column == "Group":
                character.from_group = new_value
            elif current_column == "Connections":
                character.connections = [c.strip() for c in new_value.split(",")]

            save_data(DATA_FILE, [c.to_dict() for c in characters])
            update_tree()

        if edit_window:
            edit_window.destroy()
            edit_window = None

    def on_double_click(event):
        """Handles in-cell editing via double-click."""
        nonlocal edit_window, current_item, current_column, edit_var

        if tree.identify("region", event.x, event.y) != "cell":
            return

        current_item = tree.identify_row(event.y)
        col_index = int(tree.identify_column(event.x)[1:]) - 1
        current_column = columns[col_index]
        current_value = tree.item(current_item)['values'][col_index]

        if edit_window:
            edit_window.destroy()

        edit_window = tk.Toplevel(window)
        edit_window.title(f"Edit {current_column}")
        edit_window.geometry("300x100")

        x = window.winfo_x() + event.x + 50
        y = window.winfo_y() + event.y + 50
        edit_window.geometry(f"+{x}+{y}")
        edit_var.set(current_value)

        if current_column == "Faction":
            tk.Label(edit_window, text="Select Faction:").pack(pady=5)
            global faction_combobox
            faction_combobox = ttk.Combobox(edit_window, values=faction_names, state="readonly")
            faction_combobox.set(current_value)
            faction_combobox.pack(fill="x", padx=5, pady=5)
            faction_combobox.bind("<Return>", lambda e: save_edit())
            faction_combobox.focus_set()
        else:
            entry = tk.Entry(edit_window, textvariable=edit_var)
            entry.pack(fill="x", padx=5, pady=5)
            entry.bind("<Return>", lambda e: save_edit())
            entry.focus_set()
            entry.select_range(0, tk.END)

        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(button_frame, text="Save", command=save_edit).pack(side="right", padx=5)
        tk.Button(button_frame, text="Cancel", command=lambda: edit_window.destroy()).pack(side="right", padx=5)

    # Event binding
    tree.bind("<Double-1>", on_double_click)
    update_tree()

    window.mainloop()
