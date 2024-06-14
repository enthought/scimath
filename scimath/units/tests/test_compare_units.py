from unittest import TestCase

from scimath.units.api import dimensionless, UnitArray, UnitScalar
from scimath.units.compare_units import unit_arrays_almost_equal, \
    unit_scalars_almost_equal


class TestUnitScalarAlmostEqual(TestCase):
    def test_values_identical(self):
        val1 = UnitScalar(1., units="m")
        self.assertTrue(unit_scalars_almost_equal(val1, val1))

    def test_wrong_arg_type1(self):
        val1 = 1
        val2 = UnitScalar(1., units="m")
        with self.assertRaises(ValueError):
            unit_scalars_almost_equal(val1, val2)

    def test_wrong_arg_type2(self):
        val1 = UnitScalar(1., units="m")
        val2 = 1
        with self.assertRaises(ValueError):
            unit_scalars_almost_equal(val1, val2)

    def test_values_not_close(self):
        val1 = UnitScalar(1., units="m")
        val2 = UnitScalar(1.1, units="m")
        self.assertFalse(unit_scalars_almost_equal(val1, val2))

        val2 = UnitScalar(1.00001, units="m")
        self.assertFalse(unit_scalars_almost_equal(val1, val2))

    def test_values_identical_in_diff_units(self):
        val1 = UnitScalar(1., units="m")
        val2 = UnitScalar(100., units="cm")
        self.assertTrue(unit_scalars_almost_equal(val1, val2))

    def test_dimensionless(self):
        val1 = UnitScalar(1., units=dimensionless)
        val2 = UnitScalar(1., units="cm")
        self.assertFalse(unit_scalars_almost_equal(val1, val2))

    def test_2_dimensionless(self):
        val1 = UnitScalar(1., units=dimensionless)
        val2 = UnitScalar(1., units="BLAH")
        val3 = UnitScalar(100., units="BLAH")
        self.assertTrue(unit_scalars_almost_equal(val1, val1))
        self.assertTrue(unit_scalars_almost_equal(val1, val2))
        self.assertFalse(unit_scalars_almost_equal(val1, val3))

    def test_values_close_enough(self):
        val1 = UnitScalar(1., units="m")
        val2 = val1 + UnitScalar(1.e-5, units="m")
        self.assertFalse(unit_scalars_almost_equal(val1, val2))
        self.assertTrue(unit_scalars_almost_equal(val1, val2, rtol=1e-4))


class TestUnitArraysAlmostEqual(TestCase):
    def test_wrong_argument_type1(self):
        val1 = 1
        val2 = UnitArray([1.], units="m")
        with self.assertRaises(ValueError):
            unit_arrays_almost_equal(val1, val2)

    def test_wrong_argument_type2(self):
        val1 = UnitArray([1.], units="m")
        val2 = 1
        with self.assertRaises(ValueError):
            unit_arrays_almost_equal(val1, val2)

    def test_different_shape(self):
        val1 = UnitArray([1.], units="m")
        val2 = UnitArray([1., 2.], units="m")
        self.assertFalse(unit_arrays_almost_equal(val1, val2))

    def test_not_close_default_rtol(self):
        val1 = UnitArray([1., 2.], units="m")
        val2 = UnitArray([1., 2.1], units="m")
        self.assertFalse(unit_arrays_almost_equal(val1, val2))

        val2 = UnitArray([1., 2.000001], units="m")
        self.assertFalse(unit_arrays_almost_equal(val1, val2))

    def test_values_identical(self):
        val1 = UnitArray([1., 2.], units="m")
        self.assertTrue(unit_arrays_almost_equal(val1, val1))

    def test_values_identical_in_diff_units(self):
        val1 = UnitArray([1., 2.], units="m")
        val2 = UnitArray([100., 200.], units="cm")
        self.assertTrue(unit_arrays_almost_equal(val1, val2))

    def test_dimensionless(self):
        val1 = UnitArray([1.], units=dimensionless)
        val2 = UnitArray([1.], units="cm")
        self.assertFalse(unit_arrays_almost_equal(val1, val2))

    def test_2_dimensionless(self):
        val1 = UnitArray([1.], units=dimensionless)
        val2 = UnitArray([1.], units="BLAH")
        val3 = UnitArray([100.], units="BLAH")
        self.assertTrue(unit_arrays_almost_equal(val1, val1))
        self.assertTrue(unit_arrays_almost_equal(val1, val2))
        self.assertFalse(unit_arrays_almost_equal(val1, val3))

    def test_values_close_enough(self):
        val1 = UnitArray([1., 2.], units="m")
        val2 = val1 + UnitArray([1.e-5, 1.e-6], units="m")
        self.assertFalse(unit_arrays_almost_equal(val1, val2))
        self.assertTrue(unit_arrays_almost_equal(val1, val2, rtol=1e-4))

    def test_values_not_close_enough(self):
        val1 = UnitArray([1., 2.], units="m")
        val3 = val1 + UnitArray([1.e-2, 1.e-6], units="m")
        self.assertFalse(unit_arrays_almost_equal(val1, val3, rtol=1e-4))
