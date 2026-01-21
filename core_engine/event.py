class Event:
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect

    def trigger(self, session):
        self.effect(session)