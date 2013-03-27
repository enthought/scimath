import unittest
from traits.testing.api import doctest_for_module

import scimath.units.unit_scalar as unit_scalar
from scimath.units.unit_scalar import UnitScalar
from scimath.units.length import m
from scimath.units.unit import unit


from nose.tools import assert_equal, assert_is_instance

class UnitScalarDocTestCase(doctest_for_module(unit_scalar)):
    pass


def test_offset_unit_computations():
    """ Executing some basic computations with a basic custom unit with offset.
    """
    my_u = unit(12, m.derivation, 14)
    s1 = UnitScalar(3, units=my_u)
    s2 = UnitScalar(5, units=my_u)
    s3 = s1+s2
    assert_equal(s3,UnitScalar(8, units=my_u))



if __name__ == '__main__':
    import sys
    unittest.main(argv=sys.argv)
