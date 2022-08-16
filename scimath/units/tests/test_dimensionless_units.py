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

from numpy.testing import assert_equal
from scimath.units.unit_scalar import UnitScalar
from scimath.units.unit import dimensionless


class DimensionlessTestCase(unittest.TestCase):
    def test_dimensionless(self):
        """
        Test the modification to the division, multiplication and pow
        such that a dimensionless quantity formed by is indeed dimensionless
        """

        a = UnitScalar(1.0, units='m')
        b = UnitScalar(2.0, units='mm')
        d = UnitScalar(2.0, units='m**(-1)')

        c = a / b
        e = b * d

        f = UnitScalar(2.0, units=dimensionless)
        g = f**2

        assert_equal(c.units, dimensionless)
        assert_equal(e.units, dimensionless)
        assert_equal(g.units, dimensionless)
