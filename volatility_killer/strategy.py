class Strategy:
    def __init__(self, rules):
        self.rules= rules

    def apply(self, data):
        action = None
        for rule in self.rules:
            action = rule(data)
        return action

    

