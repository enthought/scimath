# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Interpolation/Extrapolation classes.

    Policies on under-specified data fits.

    1. If the input arrays to a fit has 0 elements, numpy.NaN values
       are returned from the __call__ method for all calculated y
       values.
    2. If the input arrays to a fit class has 1 elements, this value
       is returned for all calculated y values.
"""

# major package imports
import numpy
from scipy import interpolate

# enthought imports
from traits.api import HasPrivateTraits, Bool, TraitEnum, Trait, Float

# local imports
from .interpolate import linear, logarithmic, block_average_above, window_average

# use traits for these in the future.


class DataFit(HasPrivateTraits):
    initialized = Bool(False)

    def __init__(self, x=None, y=None, **traits):
        self.initialized = False
        self._use_nans = False
        self._use_block = False
        self._x = None
        self._y = None
        if x is not None and y is not None:
            self.set_xy(x, y)
        HasPrivateTraits.__init__(self, **traits)

    def clone(self):
        new_int = self.__class__()
        new_int.__dict__.update(self.__dict__)
        return new_int

    def set_xy(self, x, y):
        x = numpy.atleast_1d(x)
        y = numpy.atleast_1d(y)

        assert len(x) == y.shape[-1], \
            "x and y arrays must have the same length"

        self.determine_special_case(x, y)
        self._x = x
        self._y = y
        self.initialized = True

    def determine_special_case(self, x, y):
        if len(x) == 0:
            self._use_nans = True
            self._use_block = False
        elif len(x) == 1:
            self._use_nans = False
            self._use_block = True
        else:
            self._use_nans = False
            self._use_block = False

    def using_special_case(self):
        return self._use_nans or self._use_block

    def calc_special_case(self, x):
        if self._use_nans is True:
            # arrays have 0 samples -- return numpy.NaN for all cases.
            y = numpy.arange(len(x)).astype(numpy.float)
            y[:] = numpy.NaN
        elif self._use_block is True:
            # arrays have 1 sample -- use it for all returned values.
            y = self.block_interp(x)
        return y

    def block_interp(self, x):
        """ Used when only one element is available in the log.
        """

        # find index of values in x that precede values in x
        # This code is a little strange -- we really want a routine that
        # returns the index of values where x[j] < x[index]
        TINY = 1e-10
        indices = numpy.searchsorted(self._x, x + TINY) - 1

        # If the value is at the front of the list, it'll have -1.
        # In this case, we will use the first (0), element in the array.
        # take requires the index array to be an Int
        indices = numpy.clip(indices, 0, numpy.Inf).astype(numpy.int)
        indices = numpy.atleast_1d(indices)
        y = numpy.take(self._y, indices, axis=-1)
        return y

    def interp(self, x):
        raise NotImplementedError("override in subclass")

    def __call__(self, x):
        if not self.initialized:
            raise ValueError("call set_xy(x, y) before trying to fit data")

        if self.using_special_case():
            y = self.calc_special_case(x)
        else:
            y = self.interp(x)

        return y

    def __eq__(self, other):
        result = True
        if self.__class__ == other.__class__:
            trait_names = other.traits()
            # fix me: added to handle new style traits
            del trait_names['trait_added']
            del trait_names['trait_modified']
            for tr in trait_names:
                if getattr(self, tr) != getattr(other, tr):
                    result = False
                    break
        else:
            result = False
        return result


class Spline(DataFit):
    """ Cubic-spline interpolation

        This class works for interpolation and extrapolation.
        !! - extrapolation seems to be broken for this
        !! - only works for 1d y arrays
    """
    # order of polynomial.  Default to cubic spline.
    order = Trait(3, TraitEnum(1, 3, 5))

    # smoothness -- larger values result in more smoothing.
    # !! I would prefer the trait to allow 0.0 and any value
    # !! between 1.0-30.0.  Values of 0.0-1.0 are *really*
    # !! CPU intensive.
    smoothness = Float(0.0)

    def __init__(self, x=None, y=None, order=3, smoothness=0):
        self.order = order
        self.smoothness = smoothness
        self._representation = None
        DataFit.__init__(self, x, y)

    def set_xy(self, x, y):
        DataFit.set_xy(self, x, y)
        if not self.using_special_case():
            # in case of exception in code below
            self.initialized = False
            if len(x) <= 3:
                # protect against short lists not having enough points
                # for a cubic-spline.
                order = 1
            else:
                order = self.order

            # catch case when order = 5 and len < 5
            if order > len(x):
                order = len(x) - 2
                # protect against even order.
                if order % 2 == 0:
                    order = order - 1

            self._representation = interpolate.splrep(x, y, k=order,
                                                      s=self.smoothness)
        self.initialized = True

    def interp(self, x):
        # !! fix for bug in splev that seg-faults if handed 1 element
        # !! array http://www.scipy.net/roundup/scipy/issue126
        scalar = False
        if len(x) == 1:
            x = numpy.array((x[0], x[0]))
            scalar = True

        y = interpolate.splev(x, self._representation, der=0)

        # !! fix for bug in splev that seg-faults if handed 1 element
        # !! array http://www.scipy.net/roundup/scipy/issue126
        if scalar:
            y = y[0]

        return numpy.atleast_1d(y)


class Linear(DataFit):

    def interp(self, x):
        return linear(self._x, self._y, x)


class Logarithmic(DataFit):

    def interp(self, x):
        return logarithmic(self._x, self._y, x)


class BlockAverageAbove(DataFit):

    def interp(self, x):
        return block_average_above(self._x, self._y, x)


class Block(DataFit):

    def interp(self, x):
        """ The base class defines a block interpolation routine to use
            for special cases.  We just use this from here.
        """
        return self.block_interp(x)


class WindowAverage(DataFit):
    width = Float(0.0)

    def __init__(self, x=None, y=None, width=10.0):
        DataFit.__init__(self, x, y, width=width)

    def interp(self, x):
        return window_average(self._x, self._y, x, width=self.width)


class EndAverage(DataFit):
    index_interval = Float(0.0)

    def __init__(self, x=None, y=None, index_interval=30.0):
        DataFit.__init__(self, x, y, index_interval=index_interval)

    def interp(self, x):
        """ Average multiple values at edges of numpy.array to use for extrapolation.

            This method only works for extrapolation.
        """
        if numpy.alltrue(numpy.logical_and(x < self._x[0], x > self._x[-1])):
            msg = "end_average() only works for extrapolation.  Some of the "\
                  "in x fall between the endpoints (x[0], x[-1]) of the "\
                  "x numpy.array."
            raise ValueError(msg)

        # find the average y value within depth_interval at both the start and
        # end of the data set that is within depth_interval distance from the
        # ends.
        indices = (self._x[0] + self.index_interval,
                   self._x[-1] - self.index_interval)
        first, last = numpy.searchsorted(self._x, indices)
        y_low = numpy.mean(self._y[:first])
        y_hi = numpy.mean(self._y[last:])

        dist_low = abs(x - self._x[0])
        dist_hi = abs(x - self._x[-1])
        y = numpy.choose(dist_low > dist_hi, (y_low, y_hi))
        return y


class FillNaN(DataFit):
    """ A DataFit which just returns all NaN's. """

    def interp(self, x):
        """ Return an numpy.array of numpy.NaN's in the same shape as x. """
        y = numpy.arange(len(x)).astype(numpy.float)
        y[:] = numpy.NaN
        return y
