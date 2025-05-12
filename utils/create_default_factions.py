import os
import json
from models.faction import Faction
from utils.data_manager import load_data, save_data

DATA_FILE = "factions.json"

def generate_default_factions():
    # Check if the file exists and is not empty
    if os.path.exists(DATA_FILE):
        try:
            existing_data = load_data(DATA_FILE)
            if existing_data:  # File exists and has data (even if it's an empty list, we proceed)
                return  # Data already exists, do nothing
        except json.JSONDecodeError:  # Handle case where the file exists but is empty or corrupted
            pass  # We will proceed to populate it with default factions

    # Default factions to initialize
    default_factions = [
        Faction(
            id=1,
            name="Mortality",
            influence=5,
            territory="Police departments, news stations, city halls",
            members=["The Aware Network", "Hunters Guild", "The Vigilant Eye"]
        ),
        Faction(
            id=2,
            name="Night",
            influence=7,
            territory="Abandoned buildings, underground clubs, cemeteries",
            members=["The Vampire Court", "Wolfpack North", "Ghost Circle"]
        ),
        Faction(
            id=3,
            name="Power",
            influence=8,
            territory="Arcane towers, libraries, hidden sanctums",
            members=["The Cabal", "The Arcane Order", "Demon Broker Syndicate"]
        ),
        Faction(
            id=4,
            name="Wild",
            influence=6,
            territory="Parks, forests, liminal spaces",
            members=["Court of Leaves", "Trickster Circle", "Elemental Assembly"]
        )
    ]

    # Save the data
    save_data(DATA_FILE, [f.to_dict() for f in default_factions])
