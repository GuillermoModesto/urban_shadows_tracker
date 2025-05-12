class Debt:
    def __init__(self, id, owed_by, owed_to, reason, status):
        self.id = id
        self.owed_by = owed_by
        self.owed_to = owed_to
        self.reason = reason
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'owed_by': self.owed_by,
            'owed_to': self.owed_to,
            'reason': self.reason,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get('id'),
            data.get('owed_by', ''),
            data.get('owed_to', ''),
            data.get('reason', ''),
            data.get('status', 'unpaid')
        )
