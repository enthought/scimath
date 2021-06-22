import unittest
import time

from numpy import arange, ones, allclose
import scipy

from scimath.interpolate.api import linear, block_average_above


class Test(unittest.TestCase):

    def assertAllclose(self, x, y):
        self.assert_(allclose(x, y))

    def test_linear(self):
        N = 3000
        x = arange(N)
        y = arange(N)
        new_x = arange(N) + 0.5
        t1 = time.clock()
        new_y = linear(x, y, new_x)
        t2 = time.clock()
        print('1d interp (sec):', t2 - t1)
        self.assertAllclose(new_y[:5], [0.5, 1.5, 2.5, 3.5, 4.5])

    def test_block_average_above(self):
        N = 3000
        x = arange(N)
        y = arange(N)

        new_x = arange(N / 2) * 2
        t1 = time.clock()
        new_y = block_average_above(x, y, new_x)
        t2 = time.clock()
        print('1d block_average_above (sec):', t2 - t1)
        self.assertAllclose(new_y[:5], [0.0, 0.5, 2.5, 4.5, 6.5])

    def test_linear2(self):
        N = 3000
        x = arange(N)
        y = ones((100, N)) * arange(N)
        new_x = arange(N) + 0.5
        t1 = time.clock()
        new_y = linear(x, y, new_x)
        t2 = time.clock()
        print('fast interpolate (sec):', t2 - t1)
        self.assertAllclose(new_y[:5, :5],
                            [[0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5],
                             [0.5, 1.5, 2.5, 3.5, 4.5]])

    def test_interp1d(self):
        N = 3000
        x = arange(N)
        y = ones((100, N)) * arange(N)
        new_x = arange(N)
        t1 = time.clock()
        interp = scipy.interpolate.interp1d(x, y)
        new_y = interp(new_x)
        t2 = time.clock()
        print('scipy interp1d (sec):', t2 - t1)
        self.assertAllclose(new_y[:5, :5],
                            [[0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4],
                             [0, 1, 2, 3, 4]])


if __name__ == '__main__':
    unittest.main()
