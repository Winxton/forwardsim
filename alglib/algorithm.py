#import talib
from oandapy import oandapy
import time
import numpy as np
import talib
from talib.abstract import *

from datetime import datetime, timedelta


"""
Similar to zipline's algorithm class
"""

class TradingAlgorithm(object):
    def __init__(self, currency_pair=None, access_token=None, *args, **kwargs):
        """
        script : str
            Algoscript that contains initialize and
            handle_data function definition.
        """

        # just one pair for now
        self.currency_pair = currency_pair

        self.oanda_client = oandapy.API(environment="practice",access_token="b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22")

        self.algoscript = kwargs.pop('script', None)

        self.data = self.oanda_client.get_prices(instruments=self.currency_pair)

        self.account_id = 3922748

        self.history_data = self.oanda_client.get_history(instrument = self.currency_pair,granularity = "S5",count = 500,candleFormat = "midpoint")


        if self.algoscript is not None:
            self.ns = {}
            exec(self.algoscript,self.ns)
            if 'initialize' not in self.ns:
                raise ValueError('You must define an initialze function.')
            if 'handle_data' not in self.ns:
                raise ValueError('You must define a handle_data function.')
            self._initialize = self.ns['initialize']
            self._handle_data = self.ns['handle_data']

        #print self.oanda_client.get_accounts()

    #Supporting Library
    def get_prices (self, **params):
        return self.oanda_client.get_history(instrument = self.currency_pair,granularity = "S5",count = 1,candleFormat = "midpoint")
    
    def convert (self, data, **params):
        candles = data["candles"]
        openArray = []
        closeArray = []
        highArray = []
        lowArray = []
        volumeArray = []

        for item in candles :
            openArray.append(item["openMid"])
            closeArray.append(item["closeMid"])
            highArray.append(item["highMid"])
            lowArray.append(item["lowMid"])
            volumeArray.append(item["volume"])

        tadic = {}
        openArray = np.asarray(openArray)

        highArray = np.asarray(highArray)

        lowArray = np.asarray(lowArray)

        closeArray = np.asarray(closeArray)

        volumeArray = np.asarray(volumeArray)

        tadic["open"] = openArray
        tadic["high"] = closeArray
        tadic["low"] = lowArray
        tadic["volume"] = volumeArray
        tadic["close"] = closeArray
        return tadic

    def stddev(self, data, **params):
        data = data['close']
        data = np.std(a=data)
        return data

    def mavg (self, data, timeperiod, **params):
        data = data['close']
        output = talib.SMA(data, timeperiod = timeperiod)
        result = output.tolist()
        avg = result[-1]
        return avg

    def order (self, units, side, **params):
        return self.oanda_client.create_order(instrument = self.currency_pair, account_id = self.account_id, units = units, side = side, type = "market")

    def get_current_close (self, **params):
        return self.oanda_client.get_history(instrument = self.currency_pair,granularity = "S5",count = 1,candleFormat = "midpoint")["candles"][0]["closeMid"]
    
    def initialize(self):
        self._initialize(self)

    def plot(self, datapoint, name):
        dataobj = [name, datapoint]
        self.plotdata['values'].append(dataobj)

    def handle_data(self, data):
        self._handle_data(self,data)

    def vwag (self, data, timeperiod, **params):
        data = data['volume']
        output = talib.WMA(data, timeperiod = timeperiod)
        result = output.tolist()
        avg = result[-1]
        return avg

    #Execution
    def run(self):
        current_timestamp = time.time()
        self.initialize()
        self.plotdata = {}

        while True:
            if (time.time() - current_timestamp) >= 5:
                self.plotdata['values'] = []
                current_price =self.get_prices()

                self.history_data["candles"].append(current_price["candles"][0])
                self.history_data["candles"].pop(0)

                data = self.convert (self.history_data)
                """
                history_dic = data.convert(self.history_data)
                avg = data.mavg(history_dic, timeperiod = 25)
                dev = data.stddev(history_dic)
                order = data.order();

                closeMid = data.get_current_close()
                print (closeMid)
                """

                current_timestamp = time.time()
                
                self.handle_data(data)

                self.plotdata['time'] = current_timestamp
                

                yield self.plotdata