import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from models.rumor import Rumor
from models.faction import Faction
from models.character import Character
from models.location import Location
from utils.data_manager import load_data, save_data
from utils.style import apply_global_styles

# File paths
DATA_FILE = "rumors.json"
FACTIONS_FILE = "factions.json"
CHARACTERS_FILE = "characters.json"
LOCATIONS_FILE = "locations.json"


def run_rumor_gui():
    """
    Launches the GUI for adding a new rumor, including related characters, factions, and locations.
    """
    window = tk.Toplevel()
    window.title("Add Rumor")
    window.geometry("300x700")
    apply_global_styles()

    # Load supporting data
    factions = [Faction.from_dict(f) for f in load_data(FACTIONS_FILE)]
    characters = [Character.from_dict(c) for c in load_data(CHARACTERS_FILE)]
    locations = [Location.from_dict(l) for l in load_data(LOCATIONS_FILE)]

    faction_names = [f.name for f in factions]
    character_names = [c.name for c in characters]
    location_names = [l.name for l in locations]

    # Input fields
    ttk.Label(window, text="Content").pack()
    content_entry = tk.Text(window, height=4, width=20)
    content_entry.pack()

    ttk.Label(window, text="Source").pack()
    source_entry = ttk.Entry(window)
    source_entry.pack()

    ttk.Label(window, text="Date Heard").pack()
    date_entry = DateEntry(window)
    date_entry.pack()

    ttk.Label(window, text="Status").pack()
    status_var = tk.StringVar()
    status_dropdown = ttk.Combobox(window, textvariable=status_var)
    status_dropdown["values"] = ("unconfirmed", "confirmed", "false", "used")
    status_dropdown.current(0)
    status_dropdown.pack()

    ttk.Label(window, text="Tags (comma-separated)").pack()
    tags_entry = ttk.Entry(window)
    tags_entry.pack()

    # Related Characters Section
    ttk.Label(window, text="Related Characters").pack()
    related_character_frame = ttk.Frame(window)
    related_character_frame.pack(fill="both", pady=5)
    related_character_comboboxes = []
    ttk.Button(
        related_character_frame,
        text="+",
        command=lambda: add_combobox(related_character_frame, related_character_comboboxes, character_names)
    ).pack(pady=5)

    # Related Factions Section
    ttk.Label(window, text="Related Factions").pack()
    related_faction_frame = ttk.Frame(window)
    related_faction_frame.pack(fill="both", pady=5)
    related_faction_comboboxes = []
    ttk.Button(
        related_faction_frame,
        text="+",
        command=lambda: add_combobox(related_faction_frame, related_faction_comboboxes, faction_names)
    ).pack(pady=5)

    # Related Locations Section
    ttk.Label(window, text="Related Locations").pack()
    related_location_frame = ttk.Frame(window)
    related_location_frame.pack(fill="both", pady=5)
    related_location_comboboxes = []
    ttk.Button(
        related_location_frame,
        text="+",
        command=lambda: add_combobox(related_location_frame, related_location_comboboxes, location_names)
    ).pack(pady=5)

    def add_combobox(parent_frame, combobox_list, options):
        """
        Adds a new dropdown (Combobox) to the given frame and stores a reference.
        """
        cb = ttk.Combobox(parent_frame, values=options)
        cb.pack(pady=5)
        combobox_list.append(cb)

    def submit():
        """
        Collects data from the form and saves the new rumor to file.
        """
        existing = [Rumor.from_dict(r) for r in load_data(DATA_FILE)]
        new_id = len(existing) + 1

        new_rumor = Rumor(
            id=new_id,
            content=content_entry.get("1.0", "end-1c"),
            source=source_entry.get(),
            date_heard=date_entry.get(),
            status=status_var.get(),
            tags=[t.strip() for t in tags_entry.get().split(",")],
            related_characters=[cb.get() for cb in related_character_comboboxes],
            related_factions=[cb.get() for cb in related_faction_comboboxes],
            related_locations=[cb.get() for cb in related_location_comboboxes],
        )

        existing.append(new_rumor)
        save_data(DATA_FILE, [r.to_dict() for r in existing])
        window.destroy()

    ttk.Button(window, text="Submit", command=submit).pack(pady=10)
    window.mainloop()
