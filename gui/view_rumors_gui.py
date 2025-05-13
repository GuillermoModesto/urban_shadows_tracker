import tkinter as tk
from tkinter import ttk
from models.rumor import Rumor
from models.character import Character
from models.faction import Faction
from models.location import Location
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "rumors.json"
CHARACTERS_FILE = "characters.json"
FACTIONS_FILE = "factions.json"
LOCATIONS_FILE = "locations.json"

def run_view_rumors_gui():
    """
    Runs the GUI for viewing and editing rumors with filterable columns and in-cell editing.
    """
    window = tk.Toplevel()
    window.title("View Rumors")

    apply_global_styles()

    # Load related data
    characters = {char.id: char.name for char in [Character.from_dict(c) for c in load_data(CHARACTERS_FILE)]}
    factions = {fac.id: fac.name for fac in [Faction.from_dict(f) for f in load_data(FACTIONS_FILE)]}
    locations = {loc.id: loc.name for loc in [Location.from_dict(l) for l in load_data(LOCATIONS_FILE)]}
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

    # Treeview setup
    tree = ttk.Treeview(window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140)
    tree.pack(expand=True, fill="both", padx=5, pady=5)

    # Variables for cell editing
    edit_window = None
    edit_var = tk.StringVar()
    current_item = None
    current_column = None

    def update_tree():
        tree.delete(*tree.get_children())
        for rumor in rumors:
            values = (
                rumor.content,
                rumor.source,
                rumor.date_heard,
                rumor.status,
                ", ".join(rumor.tags),
                ", ".join(characters.get(cid, str(cid)) for cid in rumor.related_characters),
                ", ".join(factions.get(fid, str(fid)) for fid in rumor.related_factions),
                ", ".join(locations.get(lid, str(lid)) for lid in rumor.related_locations)
            )
            tree.insert("", "end", values=values, iid=str(rumor.id))  # Explicitly setting 'iid'

    def save_edit():
        nonlocal edit_window, current_item, current_column, edit_var
        
        # Get the new value
        if current_column == "Status":
            new_value = combobox.get()  # Get value from combobox
        elif current_column == "Owed By" or current_column == "Owed To":
            new_value = combobox.get()  # Get value from combobox for characters
        else:
            new_value = edit_var.get()

        # Find the rumor by its ID
        rumor_id = int(current_item)  # Use current_item as it corresponds to the 'iid' (rumor's ID)
        rumor = next((r for r in rumors if r.id == rumor_id), None)

        if rumor:
            # Update the rumor object based on the column edited
            if current_column == "Content":
                rumor.content = new_value
            elif current_column == "Source":
                rumor.source = new_value
            elif current_column == "Date Heard":
                rumor.date_heard = new_value
            elif current_column == "Status":
                rumor.status = new_value
            elif current_column == "Tags":
                rumor.tags = [tag.strip() for tag in new_value.split(",")]
            elif current_column == "Related Characters":
                rumor.related_characters = [int(c) for c in new_value.split(",")]
            elif current_column == "Related Factions":
                rumor.related_factions = [int(f) for f in new_value.split(",")]
            elif current_column == "Related Locations":
                rumor.related_locations = [int(l) for l in new_value.split(",")]

            # Update the JSON file
            save_data(DATA_FILE, [r.to_dict() for r in rumors])

            # Refresh the treeview to reflect the changes
            update_tree()

        # Close the edit window
        if edit_window:
            edit_window.destroy()
            edit_window = None

    def on_double_click(event):
        nonlocal edit_window, current_item, current_column, edit_var
        
        # Identify the item and column clicked
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
            
        current_item = tree.identify_row(event.y)
        current_column = tree.identify_column(event.x)
        col_index = int(current_column[1:]) - 1
        current_column = columns[col_index]
        
        # Get current value
        current_values = tree.item(current_item)['values']
        current_value = current_values[col_index]
        
        # Create edit window
        if edit_window:
            edit_window.destroy()
            
        edit_window = tk.Toplevel(window)
        edit_window.title(f"Edit {current_column}")
        
        # Position near the clicked cell
        x = window.winfo_x() + event.x + 50
        y = window.winfo_y() + event.y + 50
        edit_window.geometry(f"+{x}+{y}")
        
        # Set current value
        edit_var.set(current_value)
        
        # Special handling for dropdown columns (Related Characters, Related Factions, Related Locations)
        if current_column == "Related Characters":
            label = tk.Label(edit_window, text="Select Character:")
            label.pack(pady=5)
            global combobox
            combobox = ttk.Combobox(edit_window, values=list(characters.values()), state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
        elif current_column == "Related Factions":
            label = tk.Label(edit_window, text="Select Faction:")
            label.pack(pady=5)
            combobox = ttk.Combobox(edit_window, values=list(factions.values()), state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
        elif current_column == "Related Locations":
            label = tk.Label(edit_window, text="Select Location:")
            label.pack(pady=5)
            combobox = ttk.Combobox(edit_window, values=list(locations.values()), state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
        elif current_column == "Status":
            # Add dropdown for "Status" field with predefined values
            label = tk.Label(edit_window, text="Select Status:")
            label.pack(pady=5)
            status_options = ["unconfirmed", "confirmed", "false", "used"]
            combobox = ttk.Combobox(edit_window, values=status_options, state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
        else:
            # Regular text entry for Content, Source, Date Heard, etc.
            entry = tk.Entry(edit_window, textvariable=edit_var)
            entry.pack(fill="x", padx=5, pady=5)
            entry.bind("<Return>", lambda e: save_edit())
        
        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        save_button = tk.Button(button_frame, text="Save", command=save_edit)
        save_button.pack(side="right", padx=5)
        
        cancel_button = tk.Button(button_frame, text="Cancel", 
                                command=lambda: edit_window.destroy())
        cancel_button.pack(side="right", padx=5)
        
        # Focus and select all text (for non-combobox fields)
        if current_column not in ["Related Characters", "Related Factions", "Related Locations", "Status"]:
            entry.focus_set()
            entry.select_range(0, tk.END)
        else:
            combobox.focus_set()


    # Bind double click event
    tree.bind("<Double-1>", on_double_click)

    update_tree()  # Show all rumors by default

    window.mainloop()
