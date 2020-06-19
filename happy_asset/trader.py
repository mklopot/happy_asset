from collections import deque
from position import Position
from datetime import datetime
import logging

class Trader:
    def __init__(self, backend, cash, amount_asset):
        self.open_queue = deque()
        self.closed_queue = deque()
        self.backend = backend
        
        # The size of each position
        self.amount = amount_asset


        self.cash = cash

        logging.debug("Trader initialized")

    def __str__(self):
        return "{} open: {}, closed: {}, cash: {} value: {}".format(self.backend.get_price()["Date"], len(self.open_queue), len(self.closed_queue), self.cash, self.value())

    def buy(self):
        logging.debug("Trader received 'buy' action")
        price = float(self.backend.get_price()["Low"]) * self.amount 
        if self.cash >= price:
            logging.info("Cash available, attempting to buy")
            asset = self.backend.buy(price)
            self.cash -= price
            logging.info("Purchased %s @ %s", asset, self.amount / asset)
            if asset:
                logging.debug("Buy succeeded")
                self.open_queue.appendleft(Position()) 
                self.open_queue[0].asset = asset
                self.open_queue[0].buy_price = self.amount / asset 
                self.open_queue[0].buy_timestamp = datetime.now()
                self.open_queue[0].backend = self.backend

    def sell(self):
        logging.debug("Trader received 'sell' action")
        if self.open_queue:
            logging.info("Open position available, attempting to sell")
            position = self.open_queue[-1]
            self._sell(position)

    def sell_limit(self):
        "Similar to SELL, but do not close any positions at a loss"

        logging.debug("Trader received 'sell_limit' action")
        if self.open_queue:
            logging.debug("Open position available, filtering by acceptable price")
            current_price = float(self.backend.get_price()['Low'])
            positions = list(filter(lambda p: p.buy_price < current_price, self.open_queue))
            if positions:
                position = positions[-1]
                logging.info("Found a position to close: %s", position)
                self._sell(position)

    def sell_all(self):
        while self.open_queue:
            self._sell(self.open_queue[-1])

    def _sell(self, position):
        if position in self.open_queue:
            proceeds = position.backend.sell(position.asset)
            logging.info("Sold for %s @ %s", proceeds, proceeds / position.asset)
            if proceeds:
                logging.debug("Sell succeeded")
                self.closed_queue.appendleft(self.open_queue.pop()) 
                self.closed_queue[0].sell_price = self.closed_queue[0].asset / proceeds 
                self.closed_queue[0].sell_timestamp = datetime.now()
                self.cash += proceeds

    def value(self):
        openpos_value = 0
        asset = 0
        price = float(self.backend.get_price()['Low'])
        for position in self.open_queue:
            openpos_value += position.asset * price
            asset += position.asset
        value = openpos_value + self.cash
        return {"Value": value, "Cash": self.cash, "Open": openpos_value, "Asset": asset} 
            
