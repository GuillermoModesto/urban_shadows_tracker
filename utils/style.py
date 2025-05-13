from tkinter import ttk

def apply_global_styles():
    """
    Applies a consistent style to all tkinter widgets used in the application.
    The theme is set to 'clam' for better visual contrast, and various styles 
    are applied to labels, buttons, entry fields, and treeview components.
    """
    style = ttk.Style()

    # Set the theme for the style
    style.theme_use("clam")  # 'clam' offers better visual contrast than 'default'

    # Define color palette for the application
    bg_color = "#f2f2f7"  # Light background color
    widget_bg = "#ffffff"  # White background for widgets
    accent_color = "#4a90e2"  # Soft blue for accents
    text_color = "#333333"  # Dark gray for text

    # Apply style configurations for each widget type
    style.configure("TLabel", 
                    font=("Helvetica", 12), 
                    background=bg_color, 
                    foreground=text_color, 
                    padding=5)
    
    style.configure("TEntry", 
                    font=("Helvetica", 12), 
                    padding=5)

    style.configure("TButton", 
                    font=("Helvetica", 12), 
                    padding=5, 
                    background=accent_color, 
                    foreground="white")

    style.configure("TCombobox", 
                    font=("Helvetica", 12), 
                    padding=5)

    style.configure("Treeview.Heading", 
                    font=("Helvetica", 12, "bold"), 
                    background=accent_color, 
                    foreground="white")

    style.configure("Treeview", 
                    font=("Helvetica", 11), 
                    rowheight=30, 
                    background=widget_bg, 
                    fieldbackground=widget_bg)
