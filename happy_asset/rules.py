import logging

def rule3percent_buy(data):
    logging.debug("3%-ish buy rule called")
    if data.current and data.n_back_avg(2):
        logging.debug("Evaluating data")
        if data.current < data.n_back_avg(2) * .969:
            logging.info("Signaling 'buy'")
            return "buy"
        logging.debug("No signal")
    else:
        logging.debug("Insufficient data")

def rule3percent_sell(data):
    logging.debug("3%-ish sell rule called")
    if data.current and data.n_back_avg(2):
        logging.debug("Evaluating data")
        if data.current> data.n_back_avg(2) * 1.035:
            logging.info("Signaling 'sell'")
            return "sell_limit"
        logging.debug("No signal")
    else:
        logging.debug("Insufficient data")

def uptrend_buy(data):
    logging.debug("Uptrend buy rule called")
    price7back = None
    try:
         price7back = float(data.historical[-7]['Low'])
    except:
        logging.info("Could not obtain hitorical data far enough back")

    if data.current and price7back:
        logging.debug("Evaluating data")
        logging.info("7-day gain: %f", data.current / price7back - 1)
        if data.current > price7back * 1.15:
            logging.info("Signaling 'buy'")
            return "buy"
        logging.debug("No signal")
    else:
        logging.debug("Insufficient data")

def uptrend_sell(data):
    logging.debug("Uptrend sell rule called")
    price7back = None
    try:
         price7back = float(data.historical[-7]['Low'])
    except:
        pass

    if data.current and price7back:
        logging.debug("Evaluating data")
        logging.info("7-day loss: %f", 1 - data.current / price7back)
        if data.current < price7back * .86:
            logging.info("Signaling 'sell'")
            return "sell"
        logging.debug("No signal")
    else:
        logging.debug("Insufficient data")
