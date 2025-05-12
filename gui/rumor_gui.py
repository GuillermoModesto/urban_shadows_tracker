import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from models.rumor import Rumor
from models.character import Character
from utils.data_manager import load_data, save_data

DATA_FILE = "rumors.json"
CHARACTER_FILE = "characters.json"

def run_rumor_gui():
    def add_character_dropdown():
        cb = ttk.Combobox(characters_frame, values=character_names)
        cb.pack(pady=2, fill='x')
        character_dropdowns.append(cb)

    def submit():
        selected_characters = []
        for cb in character_dropdowns:
            name = cb.get()
            if name in character_name_to_id:
                selected_characters.append(character_name_to_id[name])

        rumor = Rumor(
            id=len(load_data(DATA_FILE)) + 1,
            content=content_entry.get(),
            source=source_entry.get(),
            date_heard=date_entry.get(),
            status=status_var.get(),
            tags=[tag.strip() for tag in tags_entry.get().split(',')],
            related_characters=selected_characters,
            related_factions=[],  # You can do the same as characters here
            location_id=None  # Or apply similar logic for locations
        )
        rumors.append(rumor)
        save_data(DATA_FILE, [r.to_dict() for r in rumors])
        window.destroy()

    rumors = [Rumor.from_dict(d) for d in load_data(DATA_FILE)]

    characters = [Character.from_dict(c) for c in load_data(CHARACTER_FILE)]
    character_name_to_id = {c.name: c.id for c in characters}
    character_names = list(character_name_to_id.keys())
    character_dropdowns = []

    window = tk.Toplevel()
    window.title("Add Rumor")

    ttk.Label(window, text="Content").pack()
    content_entry = ttk.Entry(window)
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
    status_dropdown['values'] = ("unconfirmed", "confirmed", "false", "used")
    status_dropdown.current(0)
    status_dropdown.pack()

    ttk.Label(window, text="Tags (comma-separated)").pack()
    tags_entry = ttk.Entry(window)
    tags_entry.pack()

    ttk.Label(window, text="Related Characters").pack()
    characters_frame = tk.Frame(window)
    characters_frame.pack()

    add_character_dropdown()

    add_button = ttk.Button(window, text="+", command=add_character_dropdown)
    add_button.pack(pady=2)

    submit_button = ttk.Button(window, text="Submit", command=submit)
    submit_button.pack(pady=10)
