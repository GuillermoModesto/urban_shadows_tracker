import tkinter as tk
from tkinter import ttk
from models.debt import Debt
from utils.data_manager import load_data

DATA_FILE = "debts.json"

def run_view_debts_gui():
    """
    Runs the GUI for viewing debts. Displays a table with debt details including owed parties, reason, and status.
    """
    # Create a new window for viewing debts
    window = tk.Toplevel()
    window.title("View Debts")

    # Set up the Treeview widget to display debt data
    tree = ttk.Treeview(window, columns=("Owed By", "Owed To", "Reason", "Status"), show='headings')
    
    # Configure the columns for the Treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Set the heading for each column
        tree.column(col, width=120)  # Set the width for each column
    tree.pack(expand=True, fill="both")  # Pack the Treeview widget into the window

    # Load the list of debts from the data file and convert to Debt objects
    debts = [Debt.from_dict(d) for d in load_data(DATA_FILE)]  # Assuming Debt class correctly handles missing fields
    
    # Insert each debt into the Treeview
    for debt in debts:
        tree.insert("", "end", values=(
            debt.owed_by,  # Party who owes the debt
            debt.owed_to,  # Party to whom the debt is owed
            debt.reason,   # Reason for the debt
            debt.status    # Current status of the debt (e.g., unpaid, paid)
        ))

    # Start the Tkinter event loop
    window.mainloop()
