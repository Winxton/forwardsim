import numpy as np
import talib
from talib.abstract import *

from alglib.oandapy import oandapy
import time

class TradingLibrary(object):
	
	def __init__ (self) :
		self.oanda_client = oandapy.API(environment="practice",access_token="b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22")
	
	def get_prices (self, **params):
		return self.oanda_client.get_history(instrument = "EUR_USD",granularity = "S5",count = 1,candleFormat = "midpoint")
	
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
		dev = talib.STDDEV(data,price = "closeMid")
		return dev

	def mavg (self, data, timeperiod, **params):
		output = talib.SMA(data, timeperiod = timeperiod)
		return output




