
class Clause(object):
    def __init__(self, heading, sub_heading, buffer):
        self.clause = {'Main-heading': heading, 'Sub-heading': sub_heading, 'Sub-section': buffer}

    def get_clause(self):
        return self.clause
