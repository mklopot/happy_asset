import logging

def rule3percent(data):
    logging.info("Rule called")
    if data.current and data.n_back_avg(60):
        logging.info("Evaluating data")
        if data.current < data.n_back_avg(60) * .97:
            logging.info("Signaling 'buy'")
            return "buy"
        if data.current> data.n_back_avg(60) * 1.03:
            logging.info("Signaling 'sell'")
            return "sell"
        logging.info("No signal")
    else:
        logging.info("Insufficient data")

