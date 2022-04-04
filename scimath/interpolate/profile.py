# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Run timings on functions provided by scimath.interpolate.
"""

from scimath.interpolate import block_average_above, linear


def main():
    from numpy import arange, ones
    import time
    N = 3000.
    x = arange(N)
    y = arange(N)
    new_x = arange(N) + 0.5
    t1 = time.perf_counter()
    new_y = linear(x, y, new_x)
    t2 = time.perf_counter()
    print('1d interp (sec):', t2 - t1)
    print(new_y[:5])

    N = 3000.
    x = arange(N)
    y = arange(N)

    new_x = arange(N / 2) * 2
    t1 = time.perf_counter()
    new_y = block_average_above(x, y, new_x)
    t2 = time.perf_counter()
    print('1d block_average_above (sec):', t2 - t1)
    print(new_y[:5])

    N = 3000.
    x = arange(N)
    y = ones((100, int(N))) * arange(N)
    new_x = arange(N) + 0.5
    t1 = time.perf_counter()
    new_y = linear(x, y, new_x)
    t2 = time.perf_counter()
    print('fast interpolate (sec):', t2 - t1)
    print(new_y[:5, :5])

    import scipy
    N = 3000.
    x = arange(N)
    y = ones((100, int(N))) * arange(N)
    new_x = arange(N)
    t1 = time.perf_counter()
    interp = scipy.interpolate.interp1d(x, y)
    new_y = interp(new_x)
    t2 = time.perf_counter()
    print('scipy interp1d (sec):', t2 - t1)
    print(new_y[:5, :5])


if __name__ == '__main__':
    main()
