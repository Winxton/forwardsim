import numpy
from algorithm import TradingAlgorithm
import talib
from talib.abstract import *

script = """
def initialize(context):
    print "HELLO"
    context.stuff = "stuff"
    context.max = 10000

def handle_data(context):
    print "DO STUFF"
    print context.stuff
    print context.max
"""

"""
token = "b47aa58922aeae119bcc4de139f7ea1e-27de2d1074bb442b4ad2fe0d637dec22"
alg = TradingAlgorithm(token, script=script)
alg.run()
"""

"""
close = numpy.random.random(10)
print close
output = talib.SMA(close, 3)
print output
"""

# sma = abstract.Function('sma')

info = {
    'open': numpy.random.random(10),
    # 'close': numpy.random.random(10),
}

out = SMA(info, timeperiod=3, price="open")

print info
print "---"
print out


