class WorkItem:
    def __init__(self, name, effort_required):
        self.name = name
        self.effort_required = effort_required
        self.effort_done = 0
        self.completed = False

    def apply_effort(self, amount):
        self.effort_done += amount
        if self.effort_done >= self.effort_required:
            self.completed = True