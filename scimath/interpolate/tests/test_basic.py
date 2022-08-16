# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest
import time

from numpy import arange, ones, allclose
import scipy

from scimath.interpolate.api import linear, block_average_above


class Test(unittest.TestCase):

    def assertAllclose(self, x, y):
        self.assertTrue(allclose(x, y))

    def setUp(self):
        self.N = 3000
        self.x = arange(self.N)

    def test_linear(self):
        y = arange(self.N)
        new_x = arange(self.N) + 0.5
        t1 = time.perf_counter()
        new_y = linear(self.x, y, new_x)
        t2 = time.perf_counter()

        print('1d interp (sec):', t2 - t1)
        self.assertAllclose(new_y[:5], [0.5, 1.5, 2.5, 3.5, 4.5])

    def test_block_average_above(self):
        y = arange(self.N)
        new_x = arange(self.N / 2) * 2
        t1 = time.perf_counter()
        new_y = block_average_above(self.x, y, new_x)
        t2 = time.perf_counter()

        print('1d block_average_above (sec):', t2 - t1)
        self.assertAllclose(new_y[:5], [0.0, 0.5, 2.5, 4.5, 6.5])

    def test_linear2(self):
        y = ones((100, self.N)) * arange(self.N)
        new_x = arange(self.N) + 0.5
        t1 = time.perf_counter()
        new_y = linear(self.x, y, new_x)
        t2 = time.perf_counter()

        print('fast interpolate (sec):', t2 - t1)
        self.assertAllclose(new_y[:5, :5],
                            [[0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5]])

    def test_interp1d(self):
        y = ones((100, self.N)) * arange(self.N)
        new_x = arange(self.N)
        t1 = time.perf_counter()
        interp = scipy.interpolate.interp1d(self.x, y)
        new_y = interp(new_x)
        t2 = time.perf_counter()

        print('scipy interp1d (sec):', t2 - t1)
        self.assertAllclose(new_y[:5, :5],
                            [[0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4]])
