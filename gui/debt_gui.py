import tkinter as tk
from tkinter import ttk
from models.debt import Debt  # Assuming the Debt class is in models/debt.py
from utils.data_manager import load_data, save_data

DATA_FILE = "debts.json"

def run_debt_gui():
    def submit():
        # Create a Debt object using the input values
        debt = Debt(
            id=len(debts) + 1,  # Automatically generate ID based on the number of debts
            owed_by=owed_by_entry.get(),
            owed_to=owed_to_entry.get(),
            reason=reason_entry.get("1.0", "end-1c"),  # Text widget to get the multi-line reason
            status=status_var.get()
        )

        # Append the new debt to the existing list and save
        debts.append(debt)
        save_data(DATA_FILE, [d.to_dict() for d in debts])

        # Close the window after saving
        window.destroy()

    # Load existing debts from the file (or initialize as empty if the file doesn't exist)
    debts_data = load_data(DATA_FILE)
    debts = [Debt.from_dict(d) for d in debts_data]

    # Create the window for adding a new debt
    window = tk.Toplevel()
    window.title("Add Debt")

    # Owed By field
    ttk.Label(window, text="Owed By").pack()
    owed_by_entry = ttk.Entry(window)
    owed_by_entry.pack()

    # Owed To field
    ttk.Label(window, text="Owed To").pack()
    owed_to_entry = ttk.Entry(window)
    owed_to_entry.pack()

    # Reason field (multi-line text box)
    ttk.Label(window, text="Reason").pack()
    reason_entry = tk.Text(window, height=5, width=40)
    reason_entry.pack()

    # Status dropdown (unpaid, paid, partially paid)
    ttk.Label(window, text="Status").pack()
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(window, textvariable=status_var)
    status_dropdown['values'] = ("unpaid", "paid", "partially paid")
    status_dropdown.current(0)
    status_dropdown.pack()

    # Submit Button
    ttk.Button(window, text="Submit", command=submit).pack(pady=10)

    # Run the GUI event loop
    window.mainloop()
