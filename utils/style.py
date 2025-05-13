from tkinter import ttk

def apply_global_styles():
    style = ttk.Style()
    style.theme_use("clam")  # "clam" has better visual contrast than "default"

    # Light color palette
    bg_color = "#f2f2f7"
    widget_bg = "#ffffff"
    accent_color = "#4a90e2"  # Soft blue
    text_color = "#333333"

    # Apply styles
    style.configure("TLabel", font=("Helvetica", 12), background=bg_color, foreground=text_color, padding=5)
    style.configure("TEntry", font=("Helvetica", 12), padding=5)
    style.configure("TButton", font=("Helvetica", 12), padding=5, background=accent_color, foreground="white")
    style.configure("TCombobox", font=("Helvetica", 12), padding=5)
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background=accent_color, foreground="white")
    style.configure("Treeview", font=("Helvetica", 11), rowheight=30, background=widget_bg, fieldbackground=widget_bg)
