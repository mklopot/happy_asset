import importlib
import logging

import backend, strategy, data, trader, scheduler, rules

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(module)s %(funcName)s() %(message)s')
logging.info("Logging initialized")

my_backend_module = importlib.import_module("replay")
my_backend = my_backend_module.Backend()

my_strategy = strategy.Strategy([getattr(rules, "rule3percent")])
my_trader = trader.Trader(my_backend, 1, 100, True) 

my_scheduler = scheduler.Scheduler(my_trader, my_strategy, data.Data(), 0)
my_scheduler()
