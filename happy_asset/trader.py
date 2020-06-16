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
        logging.info("Trader initialized")

    def __str__(self):
        return "new: {}, open: {}, closed: {}, cash: {}".format(len(self.new_queue), len(self.open_queue), len(self.closed_queue), self.cash)

    def buy(self):
        logging.info("Trader received 'buy' action")
        if self.new_queue:
            logging.info("New position available, attempting a buy")
            asset = self.backend.buy(self.amount)
            if asset:
                logging.info("Buy succeeded")
                self.open_queue.appendleft(self.new_queue.pop()) 
                self.open_queue[0].asset = asset
                self.open_queue[0].buy_price = asset / self.amount 
                self.open_queue[0].buy_timestamp = datetime.now()
                self.open_queue[0].backend = self.backend

    def sell(self):
        logging.info("Trader received 'sell' action")
        if self.open_queue:
           position = self.open_queue[-1]
           proceeds = position.backend.sell(position.asset)
           if proceeds:
                self.closed_queue.appendleft(self.open_queue.pop()) 
                self.closed_queue[0].sell_price = self.closed_queue[0].asset / proceeds 
                self.closed_queue[0].sell_timestamp = datetime.now()
                self.cash += proceeds
                if self.recycle:
                    while self.cash >= self.amount:
                        self.new_queue.append(Position(amount=self.amount))
                        self.cash -= self.amount
               
            
            
                
        
 