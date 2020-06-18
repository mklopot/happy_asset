import logging

def rule3percent(data):
    logging.debug("Rule called")
    if data.current and data.n_back_avg(2):
        logging.debug("Evaluating data")
        if data.current < data.n_back_avg(2) * .969:
            logging.info("Signaling 'buy'")
            return "buy"
        if data.current> data.n_back_avg(2) * 1.035:
            logging.info("Signaling 'sell'")
            return "sell_limit"
        logging.debug("No signal")
    else:
        logging.debug("Insufficient data")

