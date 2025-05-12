import tkinter as tk
from tkinter import ttk
from models.debt import Debt
from utils.data_manager import load_data

DATA_FILE = "debts.json"

def run_view_debts_gui():
    window = tk.Toplevel()
    window.title("View Debts")

    tree = ttk.Treeview(window, columns=("ID", "Amount", "Owed By", "Owed To", "Due Date", "Status"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(expand=True, fill="both")

    debts = [Debt.from_dict(d) for d in load_data(DATA_FILE, Debt(0, '', '', '', 'unpaid'))]
    for debt in debts:
        tree.insert("", "end", values=(
            debt.id, debt.amount, debt.owed_by, debt.owed_to, debt.due_date, debt.status
        ))

    window.mainloop()
