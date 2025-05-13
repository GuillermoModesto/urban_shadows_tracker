from tkinter import ttk

def apply_global_styles():
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), padding=5)
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12), padding=5)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11), rowheight=30)

def apply_treeview_styles():
    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), padding=5)
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11), rowheight=30)