class QueryBase:

    def __init__(self, session):
        self.session = session

    def run(self):
        return {}
