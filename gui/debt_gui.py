import tkinter as tk
from tkinter import ttk
from models.debt import Debt
from models.character import Character
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

DATA_FILE = "debts.json"

def run_debt_gui():
    """
    Creates and displays a GUI for adding a new debt, 
    with fields for the debtor, creditor, reason, and debt status.
    """
    window = tk.Toplevel()
    window.title("Add Debt")
    
    apply_global_styles()

    def submit():
        """
        Collects the data from the input fields, creates a new Debt object,
        and saves the debt to the data file.
        """
        debt = Debt(
            id=len(debts) + 1,
            owed_by=owed_by_var.get(),
            owed_to=owed_to_var.get(),
            reason=reason_entry.get("1.0", "end-1c"),
            status=status_var.get()
        )

        # Add the new debt to the list and save it to the file
        debts.append(debt)
        save_data(DATA_FILE, [d.to_dict() for d in debts])

        # Close the window after saving the debt
        window.destroy()

    # Load existing debts from the data file
    debts_data = load_data(DATA_FILE)
    debts = [Debt.from_dict(d) for d in debts_data]

    # Load existing characters for the dropdowns
    characters = [Character.from_dict(c) for c in load_data("characters.json")]
    character_names = [char.name for char in characters]

    window.geometry("220x350")

    # Owed By field (dropdown for the debtor's name)
    ttk.Label(window, text="Owed By").pack()
    owed_by_var = tk.StringVar()
    owed_by_dropdown = ttk.Combobox(window, textvariable=owed_by_var)
    owed_by_dropdown['values'] = character_names
    owed_by_dropdown.set(character_names[0] if character_names else "")
    owed_by_dropdown.pack()

    # Owed To field (dropdown for the creditor's name)
    ttk.Label(window, text="Owed To").pack()
    owed_to_var = tk.StringVar()
    owed_to_dropdown = ttk.Combobox(window, textvariable=owed_to_var)
    owed_to_dropdown['values'] = character_names
    owed_to_dropdown.set(character_names[0] if character_names else "")
    owed_to_dropdown.pack()

    # Reason field (multi-line text box for explaining the debt)
    ttk.Label(window, text="Reason").pack()
    reason_entry = tk.Text(window, height=4, width=20)
    reason_entry.pack()

    # Status dropdown (options: unpaid, paid)
    ttk.Label(window, text="Status").pack()
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(window, textvariable=status_var)
    status_dropdown['values'] = ("unpaid", "paid")
    status_dropdown.current(0)
    status_dropdown.pack()

    # Submit button to trigger debt submission
    ttk.Button(window, text="Submit", command=submit).pack(pady=10)

    # Run the GUI event loop to display the window
    window.mainloop()
