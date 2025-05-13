class Character:
    def __init__(self, id, name, description, from_faction, from_group, connections):
        self.id = id
        self.name = name
        self.description = description
        self.from_faction = from_faction
        self.from_group = from_group
        self.connections = connections

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "from_faction": self.from_faction,
            "from_group": self.from_group,
            "connections": self.connections
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", 0),
            data.get("name", ""),
            data.get("description", ""),
            data.get("from_faction", ""),
            data.get("from_group", ""),
            data.get("connections", [])
        )
