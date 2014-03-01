import numpy
import talib

close = numpy.random.random(100)

print close

output = talib.SMA(close)

print output