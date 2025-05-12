class Location:
    def __init__(self, id, name, description, district=''):
        self.id = id
        self.name = name
        self.description = description
        self.district = district

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'district': self.district
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id'),
            data.get('name'),
            data.get('description', ''),
            data.get('district', '')  # Provide default
        )
