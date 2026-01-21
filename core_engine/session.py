class SimulationSession:
    def __init__(self, industry, start_time=0):
        self.industry = industry
        self.time = start_time
        self.work_items = []
        self.resources = {}
        self.stakeholders = []
        self.evidence_log = []

    def log(self, entry):
        self.evidence_log.append(entry)