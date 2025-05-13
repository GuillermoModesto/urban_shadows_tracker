import os
import json
from models.faction import Faction
from utils.data_manager import load_data, save_data

DATA_FILE = "factions.json"


def generate_default_factions():
    """
    Initializes the factions.json file with default factions if:
    - The file does not exist
    - The file is empty
    - The file is unreadable or corrupted (e.g. JSONDecodeError)
    """
    if os.path.exists(DATA_FILE):
        try:
            existing_data = load_data(DATA_FILE)
            if existing_data:
                return  # Valid data already exists; do nothing
        except json.JSONDecodeError:
            pass  # File is corrupted or empty; proceed with defaults

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

    save_data(DATA_FILE, [f.to_dict() for f in default_factions])
