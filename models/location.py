class Location:
    def __init__(self, id, name, description, area=None, details=None, tags=None):
        self.id = id
        self.name = name
        self.description = description
        self.area = area if area is not None else ""
        self.details = details if details is not None else ""
        self.tags = tags if tags is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "area": self.area,
            "details": self.details,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", 0),
            data.get("name", ""),
            data.get("description", ""),
            data.get("area", ""),
            data.get("details", ""),
            data.get("tags", [])
        )
