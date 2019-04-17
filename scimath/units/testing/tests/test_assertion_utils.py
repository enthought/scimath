from unittest import TestCase

from scimath.units.api import UnitArray, UnitScalar
from scimath.units.testing.assertion_utils import \
    assert_unit_array_almost_equal, assert_unit_scalar_almost_equal


class TestAssertUnitScalarEqual(TestCase):
    def test_same_unit_scalar(self):
        assert_unit_scalar_almost_equal(UnitScalar(1, units="s"),
                                        UnitScalar(1, units="s"))

    def test_equivalent_unit_scalar(self):
        assert_unit_scalar_almost_equal(UnitScalar(1, units="m"),
                                        UnitScalar(100, units="cm"))


class TestAssertUnitArrayEqual(TestCase):
    def test_same_unit_array(self):
        assert_unit_array_almost_equal(UnitArray([1, 2], units="s"),
                                       UnitArray([1, 2], units="s"))

    def test_equivalent_unit_array(self):
        assert_unit_array_almost_equal(UnitArray([1, 2], units="m"),
                                       UnitArray([100, 200], units="cm"))
