class TimeEngine:
    def __init__(self, session):
        self.session = session

    def tick(self):
        self.session.time += 1