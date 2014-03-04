#import talib
from oandapy import oandapy
import time
from library.library import TradingLibrary


"""
Similar to zipline's algorithm class
"""

class TradingAlgorithm(object):
    def __init__(self, access_token=None, currency_pair=None, *args, **kwargs):
        """
        script : str
            Algoscript that contains initialize and
            handle_data function definition.
        """

        self.oanda_client = oandapy.API(environment="practice",access_token="b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22")

        self.algoscript = kwargs.pop('script', None)

        self.data = self.oanda_client.get_prices(instruments="EUR_USD")

        self.account_id = 3922748

        self.history_data = self.oanda_client.get_history(instrument = "EUR_USD",granularity = "S5",count = 1,candleFormat = "midpoint")




        if self.algoscript is not None:
            self.ns = {}
            exec(self.algoscript, self.ns)
            if 'initialize' not in self.ns:
                raise ValueError('You must define an initialze function.')
            if 'handle_data' not in self.ns:
                raise ValueError('You must define a handle_data function.')
            self._initialize = self.ns['initialize']
            self._handle_data = self.ns['handle_data']

        # just one pair for now
        if not currency_pair:
            self.currency_pair = "EUR_USD" 

        #print self.oanda_client.get_accounts()


    def initialize(self):
        self._initialize(self)

    def handle_data(self):
        self._handle_data(self)

    def run(self):
        current_timestamp = time.time()

        while True:
            if (time.time() - current_timestamp) >= 5:
                lib = TradingLibrary()
                current_price =lib.get_prices()

                self.history_data["candles"].append(current_price["candles"][0])
                self.history_data["candles"].pop(0)

                print(self.history_data)
                """
                history_dic = lib.convert(self.history_data)
                avg = lib.mavg(history_dic,timeperiod = 25)

                print(avg)
                """
                current_timestamp = time.time()
                self.initialize()
                self.handle_data()








