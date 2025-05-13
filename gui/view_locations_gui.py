import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "locations.json"


def run_view_locations_gui():
    """
    Launches a GUI to view and edit location entries.
    - Supports filtering by column
    - Double-click to edit cells
    """
    window = tk.Toplevel()
    window.title("View Locations")
    apply_global_styles()

    columns = ("Name", "Description", "Area", "Details")
    locations = [Location.from_dict(d) for d in load_data(DATA_FILE)]

    # --- Filter Section ---
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

    # --- Treeview (Table) ---
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    # --- Editing State ---
    edit_window = None
    edit_var = tk.StringVar()
    current_item = None
    current_column = None

    def update_tree():
        tree.delete(*tree.get_children())  # Clear current tree view items
        for loc in locations:
            # Prepare the values for each location
            values = (
                loc.name,
                loc.description,
                loc.area,
                ", ".join(loc.details) if isinstance(loc.details, list) else loc.details
            )
            
            # Use loc.id or index to generate a unique 'iid' for each item
            tree.insert("", "end", values=values, iid=loc.id)  # Assuming loc.id is unique


    def save_edit():
        """Save the edited cell value and update data."""
        nonlocal edit_window, current_item, current_column

        new_value = edit_var.get()
        location_name = tree.item(current_item)['values'][0]
        location = next((l for l in locations if l.name == location_name), None)

        if location:
            if current_column == "Name":
                location.name = new_value
            elif current_column == "Description":
                location.description = new_value
            elif current_column == "Area":
                location.area = new_value
            elif current_column == "Details":
                location.details = [d.strip() for d in new_value.split(",")]

            save_data(DATA_FILE, [l.to_dict() for l in locations])
            update_tree()

        if edit_window:
            edit_window.destroy()
            edit_window = None

    def on_double_click(event):
        """Open edit popup when a cell is double-clicked."""
        nonlocal edit_window, current_item, current_column

        if tree.identify("region", event.x, event.y) != "cell":
            return

        current_item = tree.identify_row(event.y)
        col_index = int(tree.identify_column(event.x)[1:]) - 1
        current_column = columns[col_index]
        current_value = tree.item(current_item)["values"][col_index]

        if edit_window:
            edit_window.destroy()

        edit_window = tk.Toplevel(window)
        edit_window.title(f"Edit {current_column}")
        x = window.winfo_x() + event.x + 50
        y = window.winfo_y() + event.y + 50
        edit_window.geometry(f"300x100+{x}+{y}")

        edit_var.set(current_value)

        entry = tk.Entry(edit_window, textvariable=edit_var)
        entry.pack(fill="x", padx=5, pady=5)
        entry.bind("<Return>", lambda e: save_edit())
        entry.focus_set()
        entry.select_range(0, tk.END)

        btn_frame = tk.Frame(edit_window)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Save", command=save_edit).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Cancel", command=edit_window.destroy).pack(side="right", padx=5)

    tree.bind("<Double-1>", on_double_click)

    update_tree()
    window.mainloop()
