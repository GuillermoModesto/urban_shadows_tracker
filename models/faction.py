class Faction:
    def __init__(self, id, name, influence, territory, members):
        self.id = id
        self.name = name
        self.influence = influence
        self.territory = territory
        self.members = members

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "influence": self.influence,
            "territory": self.territory,
            "members": self.members
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", 0),
            data.get("name", ""),
            data.get("influence", ""),
            data.get("territory", ""),
            data.get("members", [])
        )
