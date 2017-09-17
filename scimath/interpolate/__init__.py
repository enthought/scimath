#------------------------------------------------------------------------------
# Copyright (c) 2004 by Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
""" Specialized interpolation methods for 1-D arrays, much faster than the
    standards linear interpolation in SciPy. Part of the SciMath project of
    the Enthought Tool Suite.
"""
from __future__ import absolute_import
from .interpolate import linear, block_average_above, window_average

from .fitting import DataFit, Spline, Linear, Logarithmic, BlockAverageAbove, \
    Block, EndAverage, WindowAverage, FillNaN
