import numpy

from . import _interpolate


def make_array_safe(ary, typecode):
    ary = numpy.atleast_1d(numpy.asarray(ary, typecode))
    if not ary.flags['CONTIGUOUS']:
        ary = ary.copy()
    return ary


def linear(x, y, new_x):
    """ Linearly interpolates values in new_x based on the values in x and y

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)

    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            _interpolate.linear_dddd(x, y[i], new_x, new_y[i])
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        _interpolate.linear_dddd(x, y, new_x, new_y)

    return new_y


def logarithmic(x, y, new_x):
    """ Linearly interpolates values in new_x based in the log space of y.

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)

    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            _interpolate.loginterp_dddd(x, y[i], new_x, new_y[i])
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        _interpolate.loginterp_dddd(x, y, new_x, new_y)

    return new_y


def block_average_above(x, y, new_x):
    """ Linearly interpolates values in new_x based on the values in x and y

        Parameters
        ----------
        x
            1-D array
        y
            1-D or 2-D array
        new_x
            1-D array
    """
    bad_index = None
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)

    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            bad_index = _interpolate.block_averave_above_dddd(x, y[i],
                                                              new_x, new_y[i])
            if bad_index is not None:
                break
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        bad_index = _interpolate.block_average_above_dddd(x, y, new_x, new_y)

    if bad_index is not None:
        msg = "block_average_above cannot extrapolate and new_x[%d]=%f "\
              "is out of the x range (%f, %f)" % \
              (bad_index, new_x[bad_index], x[0], x[-1])
        raise ValueError(msg)

    return new_y


def window_average(x, y, new_x, width=10.0):
    bad_index = None
    x = make_array_safe(x, numpy.float64)
    y = make_array_safe(y, numpy.float64)
    new_x = make_array_safe(new_x, numpy.float64)
    width = float(width)
    assert len(y.shape) < 3, "function only works with 1D or 2D arrays"
    if len(y.shape) == 2:
        new_y = numpy.zeros((y.shape[0], len(new_x)), numpy.float64)
        for i in range(len(new_y)):
            _interpolate.window_average_ddddd(x, y[i], new_x, new_y[i],
                                              width)
    else:
        new_y = numpy.zeros(len(new_x), numpy.float64)
        _interpolate.window_average_ddddd(x, y, new_x, new_y, width)

    return new_y


def main():
    from scipy import arange, ones
    import time
    N = 3000.
    x = arange(N)
    y = arange(N)
    new_x = arange(N) + 0.5
    t1 = time.clock()
    new_y = linear(x, y, new_x)
    t2 = time.clock()
    print('1d interp (sec):', t2 - t1)
    print(new_y[:5])

    N = 3000.
    x = arange(N)
    y = arange(N)

    new_x = arange(N / 2) * 2
    t1 = time.clock()
    new_y = block_average_above(x, y, new_x)
    t2 = time.clock()
    print('1d block_average_above (sec):', t2 - t1)
    print(new_y[:5])

    N = 3000.
    x = arange(N)
    y = ones((100, N)) * arange(N)
    new_x = arange(N) + 0.5
    t1 = time.clock()
    new_y = linear(x, y, new_x)
    t2 = time.clock()
    print('fast interpolate (sec):', t2 - t1)
    print(new_y[:5, :5])

    import scipy
    N = 3000.
    x = arange(N)
    y = ones((100, N)) * arange(N)
    new_x = arange(N)
    t1 = time.clock()
    interp = scipy.interpolate.interp1d(x, y)
    new_y = interp(new_x)
    t2 = time.clock()
    print('scipy interp1d (sec):', t2 - t1)
    print(new_y[:5, :5])

if __name__ == '__main__':
    main()
