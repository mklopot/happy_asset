class Position:
    def __init__(self):
        self.asset = 0
        self.buy_price = None
        self.sell_price = None
        self.buy_timestamp = None
        self.sell_timestamp = None
        self.backend = None

    def __str__(self):
        return "Position for {} asset, buy_price: {} at {}, sell_price: {} at {}, backend {}".format(
            self.asset,
            self.buy_price,
            self.buy_timestamp,
            self.sell_price,
            self.sell_timestamp,
            self.backend)
