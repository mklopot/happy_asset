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

    def get_price(self):
        result = self.data[self.index]
        self.index += 1
        return result
    
