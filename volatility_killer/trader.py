from collections import deque
from position import Position
from datetime import datetime

class Trader:
    def __init__(self, backend, num_positions, amount, recycle=True):
        self.new_queue = deque()
        self.open_queue = deque()
        self.closed_queue = deque()
        self.backend = backend
        self.amount = amount
        self.recycle = recycle
        self.cash = 0

        for range(num_positions):
            self.new_queue.append(Position(amount=self.amount))

    def buy(self):
        if self.new_queue:
            price = self.backend.buy(self.amount)
            if price:
                self.open_queue.appendleft(self.new_queue.pop()) 
                self.open_queue[0].buy_price = price
                self.open_queue[0].buy_timestamp = datetime.now()
                self.open_queue[0].backend = self.backend

    def sell(self):
        if self.open_queue:
           position = self.open_queue[-1]
           price = position.backend.sell(position.amount)
           if price:
                self.closed_queue.appendleft(self.open_queue.pop()) 
                self.closed_queue[0].sell_price = price
                self.closed_queue[0].sell_timestamp = datetime.now()
                self.cash += price
                if self.recycle:
                    while self.cash >= self.amount:
                        self.new_queue.append(Position(amount=self.amount))
                        self.cash -= self.amount
               
            
            
                
        
 
