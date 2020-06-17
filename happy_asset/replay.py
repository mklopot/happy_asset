import backend
import csv
from collections import deque

class Backend(backend.Backend):
    def __init__(self):
        self.current_price = None
        self.data = deque()
        self.index = 0
        with open('old_prices.csv', 'r') as f:
            price_reader = csv.DictReader(f)
            for row in price_reader:
                self.data.appendleft(row)

    def buy(self, amount):
           return amount / float(self.data[self.index]["Low"]) 

    def sell(self, asset):
           return asset * float(self.data[self.index]["Low"]) 

    def next(self):
        self.index += 1
        if self.index >= len(self.data):
            self.index = len(self.data) - 1
            return False
         

    def get_price(self):
        return self.data[self.index]
