from __future__ import absolute_import
from .interpolate import linear, block_average_above, window_average

from .fitting import DataFit, Spline, Linear, Logarithmic, BlockAverageAbove, \
                    Block, EndAverage, WindowAverage, FillNaN
