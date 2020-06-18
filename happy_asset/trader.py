from collections import deque
from position import Position
from datetime import datetime
import logging

class Trader:
    def __init__(self, backend, num_positions, amount_cents, recycle=True):
        self.new_queue = deque()
        self.open_queue = deque()
        self.closed_queue = deque()
        self.backend = backend
        
        # The size of each position
        self.amount = amount_cents

        # Create new positions with proceeds from closed positions
        self.recycle = recycle

        self.cash = 0

        for _ in range(num_positions):
            self.new_queue.append(Position(amount=self.amount))
        logging.debug("Trader initialized")

    def __str__(self):
        return "{} new: {}, open: {}, closed: {}, cash: {} value: {}".format(self.backend.get_price()["Date"], len(self.new_queue), len(self.open_queue), len(self.closed_queue), self.cash, self.value())

    def buy(self):
        logging.debug("Trader received 'buy' action")
        if self.new_queue:
            logging.info("New position available, attempting to buy")
            asset = self.backend.buy(self.amount)
            logging.info("Purchased %s @ %s", asset, self.amount / asset)
            if asset:
                logging.debug("Buy succeeded")
                self.open_queue.appendleft(self.new_queue.pop()) 
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
                if self.recycle:
                    while self.cash >= self.amount:
                        self.new_queue.append(Position(amount=self.amount))
                        self.cash -= self.amount
                        logging.info("Recycling cash into a new position, cash now %s", self.cash)

    def value(self):
        openpos_value = 0
        price = float(self.backend.get_price()['Low'])
        for position in self.open_queue:
            openpos_value += position.asset * price
        cash_value = self.amount * len(self.new_queue) + self.cash
        value = openpos_value + cash_value
        return {"Value": value, "Cash": cash_value, "Open": openpos_value} 
            
