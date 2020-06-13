import csv

class Data:
    def __init__(self, historical_csv_path=None):

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
        return sum([x["LOW"] for x in self.historical[-n:]]) / n

    def update(self, new_data):
        self.historical.append(new_data)
             
