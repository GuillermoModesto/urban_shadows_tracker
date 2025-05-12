import tkinter as tk
from tkinter import ttk
from models.debt import Debt  # Assuming the Debt class is defined in models/debt.py
from utils.data_manager import load_data, save_data

DATA_FILE = "debts.json"

def run_debt_gui():
    def submit():
        # Create a Debt object using the input values
        debt = Debt(
            id=len(debts) + 1,  # Generate a new ID based on the existing number of debts
            owed_by=owed_by_entry.get(),  # Get the name of the person who owes
            owed_to=owed_to_entry.get(),  # Get the name of the person to whom money is owed
            reason=reason_entry.get("1.0", "end-1c"),  # Get the multi-line reason from the Text widget
            status=status_var.get()  # Get the selected status from the dropdown
        )

        # Add the new debt to the list and save it to the file
        debts.append(debt)
        save_data(DATA_FILE, [d.to_dict() for d in debts])

        # Close the window after saving the debt
        window.destroy()

    # Load existing debts from the file (or initialize as empty if the file doesn't exist)
    debts_data = load_data(DATA_FILE)
    debts = [Debt.from_dict(d) for d in debts_data]

    # Create the window for adding a new debt
    window = tk.Toplevel()
    window.title("Add Debt")

    # Owed By field (single-line entry for the debtor's name)
    ttk.Label(window, text="Owed By").pack()
    owed_by_entry = ttk.Entry(window)
    owed_by_entry.pack()

    # Owed To field (single-line entry for the creditor's name)
    ttk.Label(window, text="Owed To").pack()
    owed_to_entry = ttk.Entry(window)
    owed_to_entry.pack()

    # Reason field (multi-line text box for explaining the debt)
    ttk.Label(window, text="Reason").pack()
    reason_entry = tk.Text(window, height=5, width=40)
    reason_entry.pack()

    # Status dropdown (options: unpaid, paid, partially paid)
    ttk.Label(window, text="Status").pack()
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(window, textvariable=status_var)
    status_dropdown['values'] = ("unpaid", "paid", "partially paid")
    status_dropdown.current(0)  # Default to "unpaid"
    status_dropdown.pack()

    # Submit Button to trigger debt submission
    ttk.Button(window, text="Submit", command=submit).pack(pady=10)

    # Run the GUI event loop to display the window
    window.mainloop()
