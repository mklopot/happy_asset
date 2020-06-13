from abc import ABC, abstractmethod

class Backend(ABC):
    def __init__(self, auth_info):
        pass

    @abstractmethod
    def buy(self, amount_sat):
        pass

    @abstractmethod
    def sell(self, amount_sat):
        pass

    @abstractmethod
    def get_price(self)
        pass
