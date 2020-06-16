import csv, datetime, dateparser
import logging

class Data:
    def __init__(self, historical_csv_path=None):
        self.current = None

        # Historical data in chronological order
        self.historical = []
        if historical_csv_path:
            with open(historical_csv_path, 'r') as f:
                historical_reader = csv.DictReader(f)
                for row in historical_reader:
                    self.historical.append(row)               
            self.hisotrical = self.historical.reverse()

    def n_back_avg(self, n):
        if len(self.historical) < n:
            return None 
        # Mean of daily lows
        #print([x["Low"] for x in self.historical[-n:]])
        return sum([float(x["Low"]) for x in self.historical[-n:]]) / n

    def update(self, new_data):
        logging.info("Updating data structure with new data")
        self.current = float(new_data['Low'])

        # Update historical data once per calendar day
        if not self.historical:
            logging.info("Initializing first historical data value")
            self.historical.append(new_data)
        else: 
            logging.info("New datum date %s", dateparser.parse(new_data["Date"]))
            logging.info("Last historical datum date %s", dateparser.parse(self.historical[-1]["Date"]))
            if dateparser.parse(new_data["Date"]) - dateparser.parse(self.historical[-1]["Date"]) >= datetime.timedelta(days=1):
                logging.info("Appending to historical data: interval greater than 1 day")
                self.historical.append(new_data)
            else:
                logging.info("Not appending to historical data: new value too close in time")
             
