class Decision:
    def __init__(self, description, action):
        self.description = description
        self.action = action

    def execute(self, session):
        return self.action(session)