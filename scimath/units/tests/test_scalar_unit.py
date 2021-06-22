from __future__ import absolute_import
from copy import copy
import unittest

from traits.testing.api import doctest_for_module

import scimath.units.unit_scalar as unit_scalar
from scimath.units.api import dimensionless, UnitScalar
from scimath.units.mass import gram
from scimath.units.length import m, cm
from scimath.units.unit import unit


from nose.tools import assert_equal, assert_is_instance


class UnitScalarDocTestCase(doctest_for_module(unit_scalar)):
    pass


class UnitScalarTest(unittest.TestCase):

    def test_offset_unit_computations(self):
        """ Basic computations with a basic custom unit with offset.
        """
        my_u = unit(12, m.derivation, 14)
        s1 = UnitScalar(3, units=my_u)
        s2 = UnitScalar(5, units=my_u)
        s3 = s1 + s2
        self.assertEqual(s3, UnitScalar(8, units=my_u))

    def test_repr(self):
        """ Test output of repr()"""
        a = UnitScalar(1, units="cm")
        self.assertEqual(repr(a), "UnitScalar(1, units='0.01*m')")

        # unit with no label
        labelless_unit = cm * gram
        a = UnitScalar(1, units=labelless_unit)
        self.assertEqual(repr(a), "UnitScalar(1, units='1e-05*m*kg')")

        # dimensionless quantity
        dimensionless_unit = copy(dimensionless)
        dimensionless_unit.label = "Cool unit"
        a = UnitScalar(1, units=dimensionless_unit)
        self.assertEqual(repr(a), "UnitScalar(1, units='1')")

    def test_str(self):
        """ Test output of str() """
        a = UnitScalar(1, units="cm")
        self.assertEqual(str(a), "UnitScalar (cm): 1")

        # unit with no label
        labelless_unit = cm * gram
        a = UnitScalar(1, units=labelless_unit)
        # For units with no label, the repr of the unit is used.
        self.assertEqual(str(a), "UnitScalar (1e-05*m*kg): 1")

        # dimensionless quantity
        dimensionless_unit = copy(dimensionless)
        dimensionless_unit.label = "Cool unit"
        a = UnitScalar(1, units=dimensionless_unit)
        self.assertEqual(str(a), "UnitScalar (Cool unit): 1")


def test_offset_unit_computations():
    """ Executing some basic computations with a basic custom unit with offset.
    """
    my_u = unit(12, m.derivation, 14)
    s1 = UnitScalar(3, units=my_u)
    s2 = UnitScalar(5, units=my_u)
    s3 = s1 + s2
    assert_equal(s3, UnitScalar(8, units=my_u))


if __name__ == '__main__':
    import sys
    unittest.main(argv=sys.argv)
