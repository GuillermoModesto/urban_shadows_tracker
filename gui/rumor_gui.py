import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from models.rumor import Rumor
from models.faction import Faction  # Import the Faction class
from models.character import Character  # Import the Character class
from models.location import Location  # Import the Location class
from utils.data_manager import load_data, save_data

# File paths for the data files
DATA_FILE = "rumors.json"
FACTIONS_FILE = "factions.json"
CHARACTERS_FILE = "characters.json"
LOCATIONS_FILE = "locations.json"

def run_rumor_gui():
    """
    Runs the GUI for adding a new rumor. Collects the rumor's data, related factions, characters, and locations.
    """
    # Create the main window for adding a rumor
    window = tk.Toplevel()
    window.title("Add Rumor")

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 12), padding=10)
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", font=("Helvetica", 12))
    style.configure("TCombobox", font=("Helvetica", 12))
    
    def submit():
        """
        Submits the new rumor data and saves it to the corresponding file.
        """
        # Load existing rumors data and create Rumor objects
        rumors_data = load_data(DATA_FILE)
        rumors = [Rumor.from_dict(rumor_data) for rumor_data in rumors_data]

        # Generate the next available ID for the new rumor
        new_id = len(rumors) + 1

        # Create a new Rumor object with the provided data
        rumor = Rumor(
            id=new_id,
            content=content_entry.get("1.0", "end-1c"),  # Get multi-line text from the content field
            source=source_entry.get(),
            date_heard=date_entry.get(),
            status=status_var.get(),
            tags=[tag.strip() for tag in tags_entry.get().split(',')],
            related_characters=[char_combobox.get() for char_combobox in related_character_comboboxes],
            related_factions=[faction_combobox.get() for faction_combobox in related_faction_comboboxes],
            related_locations=[location_combobox.get() for location_combobox in related_location_comboboxes]
        )

        # Append the new rumor and save the updated list
        rumors.append(rumor)
        save_data(DATA_FILE, [r.to_dict() for r in rumors])

        # Close the window after saving
        window.destroy()

    # Load data for factions, characters, and locations
    factions_data = load_data(FACTIONS_FILE)
    factions = [Faction.from_dict(faction_data) for faction_data in factions_data]
    faction_names = [faction.name for faction in factions]

    characters_data = load_data(CHARACTERS_FILE)
    characters = [Character.from_dict(character_data) for character_data in characters_data]
    character_names = [character.name for character in characters]

    locations_data = load_data(LOCATIONS_FILE)
    locations = [Location.from_dict(location_data) for location_data in locations_data]
    location_names = [location.name for location in locations]

    # Set window size (width x height)
    window.geometry("300x700")

    # Content field
    ttk.Label(window, text="Content").pack()
    content_entry = tk.Text(window, height=4, width=20)
    content_entry.pack()

    # Source field
    ttk.Label(window, text="Source").pack()
    source_entry = ttk.Entry(window)
    source_entry.pack()

    # Date Heard field (using DateEntry widget)
    ttk.Label(window, text="Date Heard").pack()
    date_entry = DateEntry(window)
    date_entry.pack()

    # Status dropdown
    ttk.Label(window, text="Status").pack()
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(window, textvariable=status_var)
    status_dropdown['values'] = ("unconfirmed", "confirmed", "false", "used")
    status_dropdown.current(0)
    status_dropdown.pack()

    # Tags field (comma-separated)
    ttk.Label(window, text="Tags (comma-separated)").pack()
    tags_entry = ttk.Entry(window)
    tags_entry.pack()

    # Related Characters Section
    related_character_frame = ttk.Frame(window)
    related_character_frame.pack(fill="both", pady=5)
    ttk.Label(related_character_frame, text="Related Characters").pack()
    related_character_comboboxes = []
    add_character_button = ttk.Button(related_character_frame, text="+", command=lambda: add_related_character_combobox(related_character_frame, related_character_comboboxes))
    add_character_button.pack(pady=5)

    # Function to add a character dropdown
    def add_related_character_combobox(parent_frame, related_character_comboboxes):
        char_combobox = ttk.Combobox(parent_frame, values=character_names)
        char_combobox.pack(pady=5)
        related_character_comboboxes.append(char_combobox)

    # Related Factions Section
    related_faction_frame = ttk.Frame(window)
    related_faction_frame.pack(fill="both", pady=5)
    ttk.Label(related_faction_frame, text="Related Factions").pack()
    related_faction_comboboxes = []
    add_faction_button = ttk.Button(related_faction_frame, text="+", command=lambda: add_related_faction_combobox(related_faction_frame, related_faction_comboboxes))
    add_faction_button.pack(pady=5)

    # Function to add a faction dropdown
    def add_related_faction_combobox(parent_frame, related_faction_comboboxes):
        faction_combobox = ttk.Combobox(parent_frame, values=faction_names)
        faction_combobox.pack(pady=5)
        related_faction_comboboxes.append(faction_combobox)

    # Related Locations Section
    related_location_frame = ttk.Frame(window)
    related_location_frame.pack(fill="both", pady=5)
    ttk.Label(related_location_frame, text="Related Locations").pack()
    related_location_comboboxes = []
    add_location_button = ttk.Button(related_location_frame, text="+", command=lambda: add_related_location_combobox(related_location_frame, related_location_comboboxes))
    add_location_button.pack(pady=5)

    # Function to add a location dropdown
    def add_related_location_combobox(parent_frame, related_location_comboboxes):
        location_combobox = ttk.Combobox(parent_frame, values=location_names)
        location_combobox.pack(pady=5)
        related_location_comboboxes.append(location_combobox)

    # Submit button to save the rumor
    ttk.Button(window, text="Submit", command=submit).pack(pady=10)

    # Start the event loop for the window
    window.mainloop()
