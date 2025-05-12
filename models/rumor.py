class Rumor:
    def __init__(self, id, content, source, date_heard, status, tags, related_characters, related_factions, related_locations):
        self.id = id
        self.content = content
        self.source = source
        self.date_heard = date_heard
        self.status = status
        self.tags = tags
        self.related_characters = related_characters
        self.related_factions = related_factions
        self.related_locations = related_locations  # Ensure this is present

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "source": self.source,
            "date_heard": self.date_heard,
            "status": self.status,
            "tags": self.tags,
            "related_characters": self.related_characters,
            "related_factions": self.related_factions,
            "related_locations": self.related_locations
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("id", 0),
            data.get("content", ""),
            data.get("source", ""),
            data.get("date_heard", ""),
            data.get("status", "unconfirmed"),
            data.get("tags", []),
            data.get("related_characters", []),
            data.get("related_factions", []),
            data.get("related_locations", [])
        )
