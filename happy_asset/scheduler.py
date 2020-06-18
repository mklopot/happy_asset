import time, logging

class Scheduler:
    def __init__(self, trader, strategy, data, interval):
        self.trader = trader
        self.strategy = strategy
        self.data = data
        self.interval = interval

    def tick(self):
            if self.trader.backend.next() is not False:
                price = self.trader.backend.get_price()
                if price:
                    self.data.update(price)    
                    action = self.strategy.apply(self.data)
                    if action:
                        logging.debug("Passing action to trader: %s", action)
                        getattr(self.trader, action, None)()
                        self.info()

                    # Keep track of how well the trader is doing
                    value = self.trader.value()
                    value["Date"] = price["Date"]
                    self.data.historical_value.append(value)
            else:
                logging.info("Could not advance backend to next datum, generating a graph and exiting")
                self.info()
                self.data.graph()
                exit()
         
            

    def info(self):
        print(self.trader)

    def __call__(self):
        while True:
            self.tick()
            time.sleep(self.interval)        
