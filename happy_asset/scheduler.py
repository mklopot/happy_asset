import time, logging

class Scheduler:
    def __init__(self, trader, strategy, data, interval):
        self.trader = trader
        self.strategy = strategy
        self.data = data
        self.interval = interval

    def tick(self):
        self.data.update(self.trader.backend.get_price())    
        action = self.strategy.apply(self.data)
        if action:
            logging.debug("Passing action to trader: %s", action)
            getattr(self.trader, action, None)()
        self.info()

    def info(self):
        print(self.trader)

    def __call__(self):
        while True:
            self.tick()
            time.sleep(self.interval)        
