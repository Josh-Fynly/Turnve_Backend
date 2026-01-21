from .time import TimeEngine

class SimulationEngine:
    def __init__(self, session):
        self.session = session
        self.time_engine = TimeEngine(session)

    def step(self):
        self.time_engine.tick()
