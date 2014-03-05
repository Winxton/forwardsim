import numpy as np
import talib
from talib.abstract import *

from alglib.oandapy import oandapy
import time
from datetime import datetime, timedelta

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
		data = data['close']
		data = np.std(a=data)
		return data

	def mavg (self, data,timeperiod, **params):
		data = data['close']
		output = talib.SMA(data, timeperiod = timeperiod)
		result = output.tolist()
		avg = result[-1]
		return avg

	def order (self, units, side, **params):
		trade_expire = datetime.now() + timedelta(days=1)
		trade_expire = trade_expire.isoformat("T") + "Z"
		return self.oanda_client.create_order(instrument = "EUR_USD", account_id = 3922748, units = units, side = side, type = "limit", expiry = trade_expire, price = 1.15)

	def get_current_close (self, **params):
		return self.oanda_client.get_history(instrument = "EUR_USD",granularity = "S5",count = 1,candleFormat = "midpoint")["candles"][0]["closeMid"]




