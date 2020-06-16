class Position:
    def __init__(self, amount):
        # Dollar amount of the position
        self.amount = amount

        self.asset = 0
        self.buy_price = None
        self.sell_price = None
        self.buy_timestamp = None
        self.sell_timestamp = None
        self.backend = None
