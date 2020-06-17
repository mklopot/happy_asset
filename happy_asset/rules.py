import logging

def rule3percent(data):
    logging.debug("Rule called")
    if data.current and data.n_back_avg(2):
        logging.debug("Evaluating data")
        if data.current < data.n_back_avg(2) * .97:
            logging.info("Signaling 'buy'")
            return "buy"
        if data.current> data.n_back_avg(2) * 1.04:
            logging.info("Signaling 'sell'")
            return "sell_limit"
        logging.info("No signal")
    else:
        logging.debug("Insufficient data")

