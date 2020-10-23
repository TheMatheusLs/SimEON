


class Schedule:
    def __init__(self, parent, *args, **kwargs):

        self.parent = parent

    def initialise(self):
        self.first_event = None
        self.sim_time = 0.0