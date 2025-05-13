import tkinter as tk
from tkinter import ttk
from models.debt import Debt
from models.character import Character
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "debts.json"
CHARACTERS_FILE = "characters.json"


def run_view_debts_gui():
    """
    Launches a GUI for viewing and editing debts.
    Features:
    - Column-based filtering
    - In-cell editing
    - Dropdowns for characters and status fields
    """
    window = tk.Toplevel()
    window.title("View Debts")
    apply_global_styles()

    characters = [Character.from_dict(c) for c in load_data(CHARACTERS_FILE)]
    character_names = [c.name for c in characters]
    debts = [Debt.from_dict(d) for d in load_data(DATA_FILE)]

    columns = ("Owed By", "Owed To", "Reason", "Status")

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

    # Edit state
    edit_window = None
    edit_var = tk.StringVar()
    current_item = None
    current_column = None

    def update_tree():
        """Refreshes the treeview based on filters."""
        tree.delete(*tree.get_children())
        for debt in debts:
            values = (debt.owed_by, debt.owed_to, debt.reason, debt.status)
            if all(filter_vars[col].get().lower() in str(values[i]).lower() for i, col in enumerate(columns)):
                tree.insert("", "end", values=values, iid=str(debt.id))

    def save_edit():
        """Saves the edited value and updates the data file."""
        nonlocal edit_window, current_item, current_column

        new_value = combobox.get() if current_column in {"Owed By", "Owed To", "Status"} else edit_var.get()
        debt_id = int(current_item)
        debt = next((d for d in debts if d.id == debt_id), None)

        if debt:
            if current_column == "Owed By":
                debt.owed_by = new_value
            elif current_column == "Owed To":
                debt.owed_to = new_value
            elif current_column == "Reason":
                debt.reason = new_value
            elif current_column == "Status":
                debt.status = new_value

            save_data(DATA_FILE, [d.to_dict() for d in debts])
            update_tree()

        if edit_window:
            edit_window.destroy()
            edit_window = None

    def on_double_click(event):
        """Triggers an in-cell edit window."""
        nonlocal edit_window, current_item, current_column, edit_var

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

        # ComboBoxes for certain columns
        if current_column in {"Owed By", "Owed To"}:
            tk.Label(edit_window, text=f"Select {current_column}:").pack(pady=5)
            global combobox
            combobox = ttk.Combobox(edit_window, values=character_names, state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
            combobox.focus_set()
        elif current_column == "Status":
            tk.Label(edit_window, text="Select Status:").pack(pady=5)
            combobox = ttk.Combobox(edit_window, values=["unpaid", "paid"], state="readonly")
            combobox.set(current_value)
            combobox.pack(fill="x", padx=5, pady=5)
            combobox.bind("<Return>", lambda e: save_edit())
            combobox.focus_set()
        else:
            entry = tk.Entry(edit_window, textvariable=edit_var)
            entry.pack(fill="x", padx=5, pady=5)
            entry.bind("<Return>", lambda e: save_edit())
            entry.focus_set()
            entry.select_range(0, tk.END)

        # Buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack(fill="x", padx=5, pady=5)
        tk.Button(button_frame, text="Save", command=save_edit).pack(side="right", padx=5)
        tk.Button(button_frame, text="Cancel", command=edit_window.destroy).pack(side="right", padx=5)

    tree.bind("<Double-1>", on_double_click)
    update_tree()
    window.mainloop()
