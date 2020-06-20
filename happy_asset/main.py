import importlib
import logging

import backend, rules, data, trader, scheduler, rules

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(module)s %(funcName)s() %(message)s')
logging.info("Logging initialized")

my_backend_module = importlib.import_module("replay")
my_backend = my_backend_module.Backend()

rules = [getattr(rules, "rule3percent_sell"),
         getattr(rules, "uptrend_buy"),
         getattr(rules, "rule3percent_buy")
        ]
#         getattr(rules, "uptrend_sell")]

my_trader = trader.Trader(my_backend, 300, .1) 

my_scheduler = scheduler.Scheduler(my_trader, rules, data.Data(), 0)
my_scheduler()
