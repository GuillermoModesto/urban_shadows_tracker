import tkinter as tk
from tkinter import ttk
from tkinter import font

# Importing the relevant functions for different categories
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
from utils.data_manager import ensure_files_exist
from utils.create_default_factions import generate_default_factions

def create_tile(parent, title, add_command, view_command, row, col):
    """
    Creates a tile containing Add and View buttons for each category (Rumor, Character, etc.)
    The tile is added to a grid within the given parent frame.
    """
    # Create a frame for the tile with specific dimensions and background color
    frame = tk.Frame(parent, relief="solid", bd=2, width=180, height=180, bg="#f0f0f0")
    frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    # Make the frame expand within the grid layout
    parent.grid_rowconfigure(row, weight=1, uniform="equal")
    parent.grid_columnconfigure(col, weight=1, uniform="equal")

    # Title label for the tile
    title_label = tk.Label(frame, text=title, font=("Arial", 14), bg="#3498db", fg="white", anchor="center")
    title_label.pack(fill="x", pady=5)

    # Button to add a new entry for the category
    button_add = ttk.Button(frame, text="Add", command=add_command)
    button_add.pack(fill="x", pady=5)

    # Button to view all entries for the category
    button_view = ttk.Button(frame, text="View", command=view_command)
    button_view.pack(fill="x", pady=5)

def run_main_gui():
    """ 
    Runs the main GUI window which contains tiles for each category (Rumor, Character, etc.)
    Each tile has an 'Add' and 'View' button for managing data.
    """
    ensure_files_exist()  # Ensure all necessary data files exist
    generate_default_factions()  # Generate default factions if needed

    # Create the main window
    window = tk.Tk()
    window.title("Urban Shadows Tracker")

    # Create a main frame to hold all the category tiles
    main_frame = tk.Frame(window)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Set up grid layout for the tiles (adjust number of columns and rows as needed)
    num_columns = 3  # Number of columns for tiles
    num_rows = 2     # Number of rows for tiles

    # Create the tiles for each category
    create_tile(main_frame, "Rumor", run_rumor_gui, run_view_rumors_gui, 0, 0)
    create_tile(main_frame, "Character", run_character_gui, run_view_characters_gui, 0, 1)
    create_tile(main_frame, "Faction", run_faction_gui, run_view_factions_gui, 0, 2)
    create_tile(main_frame, "Location", run_location_gui, run_view_locations_gui, 1, 0)
    create_tile(main_frame, "Debt", run_debt_gui, run_view_debts_gui, 1, 1)

    # Start the main event loop of the GUI
    window.mainloop()
