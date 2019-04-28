from unittest import TestCase

from scimath.units.api import UnitArray, UnitScalar
from scimath.units.assertion_utils import assert_unit_array_almost_equal, \
    assert_unit_scalar_almost_equal


class TestAssertUnitScalarEqual(TestCase):
    def test_same_unit_scalar(self):
        assert_unit_scalar_almost_equal(UnitScalar(1, units="s"),
                                        UnitScalar(1, units="s"))

    def test_equivalent_unit_scalar(self):
        assert_unit_scalar_almost_equal(UnitScalar(1, units="m"),
                                        UnitScalar(100, units="cm"))

    def test_not_close(self):
        with self.assertRaises(AssertionError):
            assert_unit_scalar_almost_equal(UnitScalar(1, units="m"),
                                            UnitScalar(1.1, units="m"))

    def test_not_close_custom_msg(self):
        a1 = UnitScalar(1, units="m")
        a2 = UnitScalar(1.1, units="m")
        with self.assertRaises(AssertionError):
            assert_unit_scalar_almost_equal(a1, a2, rtol=1e-2, msg="BLAH")

    def test_unit_scalar_non_default_rtol(self):
        assert_unit_scalar_almost_equal(UnitScalar(1, units="m"),
                                        UnitScalar(1.01, units="m"), rtol=1e-1)


class TestAssertUnitArrayEqual(TestCase):
    def test_same_unit_array(self):
        assert_unit_array_almost_equal(UnitArray([1, 2], units="s"),
                                       UnitArray([1, 2], units="s"))

    def test_equivalent_unit_array(self):
        assert_unit_array_almost_equal(UnitArray([1, 2], units="m"),
                                       UnitArray([100, 200], units="cm"))

    def test_not_close(self):
        a1 = UnitArray([1.01, 2], units="s")
        a2 = UnitArray([1, 2], units="s")
        with self.assertRaises(AssertionError):
            assert_unit_array_almost_equal(a1, a2)

    def test_not_close_custom_msg(self):
        a1 = UnitArray([1.01, 2], units="s")
        a2 = UnitArray([1, 2], units="s")
        with self.assertRaises(AssertionError):
            assert_unit_array_almost_equal(a1, a2, msg="BLAH")

    def test_unit_scalar_non_default_rtol(self):
        assert_unit_array_almost_equal(UnitScalar(1, units="m"),
                                       UnitScalar(1.01, units="m"), rtol=1e-1)
