class Action:
    def __init__(self, description: str):
        self.description = description

    def __repr__(self):
        return self.description