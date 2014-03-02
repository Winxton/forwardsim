import talib
from oandapy import oandapy
"""
Similar to zipline's algorithm class
"""

class TradingAlgorithm(object):
    def __init__(self, access_token, currency_pair=None, *args, **kwargs):
        """
        script : str
            Algoscript that contains initialize and
            handle_data function definition.
        """

        self.oanda_client = oandapy.API(environment="practice", access_token=access_token)

        self.algoscript = kwargs.pop('script', None)

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

        print self.oanda_client.get_accounts()


    def initialize(self):
        self._initialize(self)

    def handle_data(self):
        self._handle_data(self)

    def run(self):
        self.initialize()
        self.handle_data()