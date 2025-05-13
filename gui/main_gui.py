import tkinter as tk
from tkinter import ttk

from gui.rumor_gui import run_rumor_gui
from gui.view_rumors_gui import run_view_rumors_gui
from gui.character_gui import run_character_gui
from gui.view_characters_gui import run_view_characters_gui
from gui.faction_gui import run_faction_gui
from gui.view_factions_gui import run_view_factions_gui
from gui.location_gui import run_location_gui
from gui.view_locations_gui import run_view_locations_gui
from gui.debt_gui import run_debt_gui
from gui.view_debts_gui import run_view_debts_gui
from utils.data_manager import ensure_user_data_exists
from utils.create_default_factions import generate_default_factions
from utils.style import apply_global_styles


def create_tile(parent, title, add_command, view_command, row, col):
    """
    Creates a single dashboard tile with an Add and View button for a specific category.

    Args:
        parent (tk.Widget): Parent container to place the tile in.
        title (str): Title to display at the top of the tile.
        add_command (function): Function to call when "Add" is clicked.
        view_command (function): Function to call when "View" is clicked.
        row (int): Row index in the grid.
        col (int): Column index in the grid.
    """
    frame = tk.Frame(parent, relief="solid", bd=2, width=180, height=180, bg="#f0f0f0")
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
    parent.grid_rowconfigure(row, weight=1, uniform="equal")
    parent.grid_columnconfigure(col, weight=1, uniform="equal")

    title_label = tk.Label(frame, text=title, font=("Arial", 14), bg="#3498db", fg="white", anchor="center")
    title_label.pack(fill="x")

    inner_frame = tk.Frame(frame, bg="#f0f0f0")
    inner_frame.pack(expand=True, fill="both", padx=10, pady=10)

    button_add = ttk.Button(inner_frame, text="Add", command=add_command)
    button_add.pack(fill="x", pady=5)

    button_view = ttk.Button(inner_frame, text="View", command=view_command)
    button_view.pack(fill="x", pady=5)

    apply_global_styles()


def run_main_gui():
    """
    Launches the main dashboard window of the Urban Shadows Tracker.
    Displays tiles for each data category, each with Add and View options.
    """
    ensure_user_data_exists()
    generate_default_factions()

    window = tk.Tk()
    window.title("Urban Shadows Tracker")

    main_frame = tk.Frame(window)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    create_tile(main_frame, "Rumor", run_rumor_gui, run_view_rumors_gui, 0, 0)
    create_tile(main_frame, "Character", run_character_gui, run_view_characters_gui, 0, 1)
    create_tile(main_frame, "Faction", run_faction_gui, run_view_factions_gui, 0, 2)
    create_tile(main_frame, "Location", run_location_gui, run_view_locations_gui, 1, 0)
    create_tile(main_frame, "Debt", run_debt_gui, run_view_debts_gui, 1, 1)

    window.mainloop()
