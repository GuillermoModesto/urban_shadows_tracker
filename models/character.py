class Character:
    def __init__(self, id, name, description, connections):
        self.id = id
        self.name = name
        self.description = description
        self.connections = connections

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "connections": self.connections
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", 0),
            data.get("name", ""),
            data.get("description", ""),
            data.get("connections", [])
        )
