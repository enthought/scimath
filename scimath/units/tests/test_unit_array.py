# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Standard library imports
from copy import copy
from pickle import dumps, loads
import timeit
import unittest
import operator

# Numeric library imports
import numpy
from numpy import all, array, sqrt
from numpy.testing import assert_array_equal

# Enthought Library imports
import scimath.units as units
from scimath.units.length import cm, feet, meters
from scimath.units.mass import gram
from scimath.units.time import second, seconds
from scimath.units.unit import InvalidConversion, dimensionless

# Numerical modeling library imports
from scimath.units.api import UnitArray, UnitScalar


class UnitArrayTestCase(unittest.TestCase):

    ##########################################################################
    # Test construction from arrays
    ##########################################################################

    def test_create_1d_from_list(self):
        """ Create an array from a 1D list.
        """
        a = UnitArray([1, 2, 3])
        assert(a[0] == 1)

    def test_create_2d_from_list(self):
        """ Create an array from a 2D list.
        """
        a = UnitArray([[1, 2, 3],
                       [4, 5, 6]])
        assert(a[1, 2] == 6)

    ############################################################################
    # Test construction from arrays
    ############################################################################

    def test_repr(self):
        """ Test output of repr()"""
        a = UnitArray([1, 2, 3], units="cm")
        self.assertEqual(repr(a), "UnitArray([1, 2, 3], units='0.01*m')")

        # unit with no label
        labelless_unit = cm * gram
        a = UnitArray([1, 2, 3], units=labelless_unit)
        self.assertEqual(repr(a), "UnitArray([1, 2, 3], units='1e-05*m*kg')")

        # dimensionless quantity
        dimensionless_unit = copy(dimensionless)
        dimensionless_unit.label = "Cool unit"
        a = UnitArray([1, 2, 3], units=dimensionless_unit)
        self.assertEqual(repr(a), "UnitArray([1, 2, 3], units='1')")

    def test_str(self):
        """ Test output of str() """
        a = UnitArray([1, 2, 3], units="cm")
        self.assertEqual(str(a), "UnitArray (cm): [1, 2, 3]")

        # unit with no label
        labelless_unit = cm * gram
        a = UnitArray([1, 2, 3], units=labelless_unit)
        # For units with no label, the repr of the unit is used.
        self.assertEqual(str(a), "UnitArray (1e-05*m*kg): [1, 2, 3]")

        # dimensionless quantity
        dimensionless_unit = copy(dimensionless)
        dimensionless_unit.label = "Cool unit"
        a = UnitArray([1, 2, 3], units=dimensionless_unit)
        self.assertEqual(str(a), "UnitArray (Cool unit): [1, 2, 3]")

    ##########################################################################
    # Test mathematical operations
    ##########################################################################

    def test_sin(self):
        """ Unary operation on a UnitArray should return a UnitArray.
        """
        a = UnitArray([1, 2, 3])
        res = numpy.sin(a)  # @UndefinedVariable
        assert (isinstance(res, UnitArray))

    def test_add(self):
        """ Binary operation of array + UnitArray should return a UnitArray.
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary)
        res = unit_ary + ary
        assert isinstance(res, UnitArray)

    def test_array_equality(self):
        """ Rich comparison of array == UnitArray should compare the data
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary)
        res = unit_ary + ary
        assert numpy.all(res == (ary + ary))

    ##########################################################################
    # Tests for units
    ##########################################################################

    def test_units_default(self):
        """ Are their units on this UnitArray.
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary)
        self.assertEqual(unit_ary.units, None)

    def test_units_init(self):
        """ Are their units on this UnitArray.
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary, units=dimensionless)
        self.assertEqual(unit_ary.units, dimensionless)

    def test_as_units(self):
        """ Conversion from one unit system to another.
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary, units=meters)
        new_unit_ary = unit_ary.as_units(feet)

        # Test the values are correct
        desired_array = units.convert(ary, meters, feet)
        self.assertTrue(numpy.all(desired_array == new_unit_ary))

        # Also, make sure the units are correctly assigned.
        self.assertEqual(new_unit_ary.units, feet)

        # fixme: We should also test that any other items in the unit_ary are
        #        copied.

    ##########################################################################
    # Test cloning type behavior.
    ##########################################################################

    def test_slice_keeps_attributes(self):
        """ Does a sliced version of a UnitArray keeps its attributes?
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary, units=meters)
        new_unit_ary = unit_ary[:2]

        # Also, make sure the units and family_name are correctly assigned.
        self.assertEqual(new_unit_ary.units, meters)

    def test_add_keeps_attributes(self):
        """ In "new=UnitArray+ary", new should have attributes of UnitArray.
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary, units=meters)
        new_unit_ary = ary + unit_ary

        # Also, make sure the units and family_name are correctly assigned.
        self.assertEqual(new_unit_ary.units, meters)

    def test_concatenate(self):
        unit_ary_1 = UnitArray(numpy.array((1, 2, 3)), units=meters)
        unit_ary_2 = UnitArray(numpy.array((4, 5, 6)), units=meters)

        new_unit_ary = UnitArray.concatenate([unit_ary_1, unit_ary_2])
        expected = UnitArray((1, 2, 3, 4, 5, 6), units=meters)
        self.assertTrue(numpy.all(new_unit_ary == expected))

    def test_concatenate_keeps_attribute(self):
        """ concatenating does not call __new__ on the result
            so the attribute must be set correctly in __array_finalize__
        """
        unit_ary_1 = UnitArray(numpy.array((1, 2, 3)), units=meters)
        unit_ary_2 = UnitArray(numpy.array((1, 2, 3)), units=meters)

        new_unit_ary = UnitArray.concatenate([unit_ary_1, unit_ary_2])

        self.assertEqual(new_unit_ary.units, meters)

    def test_concatenate_keeps_attribute_using_mixed_units(self):
        """ concatenating does not call __new__ on the result
            so the attribute must be set correctly in __array_finalize__.
            This test creates another unit array with different units
            before the concatenate to make sure the finalize method does not
            assign the wrong units
        """
        unit_ary_1 = UnitArray(numpy.array((1, 2, 3)), units=meters)
        unit_ary_2 = UnitArray(numpy.array((1, 2, 3)), units=meters)

        unit_ary_3 = UnitArray(numpy.array((1, 2, 3)), units=feet)
        new_unit_ary = UnitArray.concatenate([unit_ary_1, unit_ary_2])

        self.assertEqual(new_unit_ary.units, meters)

    ##########################################################################
    # Test mathematical operations
    ##########################################################################

    def test_index_name(self):
        """ Can set and retreive the index_name?
        """
        ary = numpy.array((1, 2, 3))
        unit_ary = UnitArray(ary)
        unit_ary.index_name = "depth"
        self.assertEqual(unit_ary.index_name, "depth")


class UnitArrayPickleTestCase(unittest.TestCase):

    def test_pickle(self):
        'Pickling'
        for a in (

            UnitArray(0),
            UnitArray([0, 1]),
            UnitArray([0, 1], units=feet / seconds),
            UnitArray([[0.5, 1.0], [10., 20.]], units=meters),

        ):
            state = dumps(a)
            b = loads(state)
            self.assertTrue(all(b == a))
            self.assertTrue(hasattr(b, 'units'))
            self.assertEqual(b.units, a.units)


class PassUnitsTestCase(unittest.TestCase):
    """ Some ufuncs keep units.
    """

    ##########################################################################
    # ConvertUnitsTestCase interface.
    ##########################################################################

    def test_add(self):
        a = UnitArray([1, 2, 3], units=meters / second)
        b = UnitArray([1, 2, 3], units=meters / second)
        result = a + b
        self.assertEqual(result.units, meters / second)

    def test_add_compatible(self):
        a = UnitArray([1, 2, 3], units=meters)
        b = UnitArray([1, 2, 3], units=feet)
        result = a + b
        mplusf = (meters + feet).value
        self.assertEqual(result[0], mplusf)
        self.assertEqual(result.units, meters)

    def test_add_nopass(self):
        a = UnitArray([1, 2, 3], units=meters / second)
        b = UnitArray([1, 2, 3], units=feet)
        self.assertRaises(InvalidConversion, operator.add, a, b)

    def test_subtract(self):
        a = UnitArray([1, 2, 3], units=meters / second)
        b = UnitArray([1, 2, 3], units=meters / second)
        result = a - b
        self.assertEqual(result.units, meters / second)

    def test_subtract_compatible(self):
        a = UnitArray([1, 2, 3], units=meters)
        b = UnitArray([1, 2, 3], units=feet)
        result = a - b
        mminusf = (meters - feet).value
        self.assertEqual(result[0], mminusf)
        self.assertEqual(result.units, meters)

    def test_subtract_dimensionless(self):
        a = UnitArray([1, 2, 3], units=dimensionless)
        b = 1
        result = a - b
        self.assertEqual(result.units, dimensionless)
        assert_array_equal(result, UnitArray([0, 1, 2], units=dimensionless))
        result = b - a
        self.assertEqual(result.units, dimensionless)
        assert_array_equal(result, UnitArray([0, -1, -2], units=dimensionless))
        c = array([3, 2, 1])
        result = a - c
        self.assertEqual(result.units, dimensionless)
        assert_array_equal(result, UnitArray([-2, 0, 2], units=dimensionless))
        result = c - a
        self.assertEqual(result.units, dimensionless)
        assert_array_equal(result, UnitArray([2, 0, -2], units=dimensionless))

    def test_divide_pass(self):
        a = UnitArray([1, 2, 3], units=meters / second)
        result = a / 3.0
        self.assertEqual(result.units, meters / second)
        result = 3.0 / a
        self.assertEqual(result.units, second / meters)
        b = UnitArray([3, 2, 1], units=second)
        result = a / b
        self.assertEqual(result.units, meters / second**2)

    def test_multiply_pass(self):
        a = UnitArray([1, 2, 3], units=meters / second)
        result = a * 3.0
        self.assertEqual(result.units, meters / second)
        result = 3.0 * a
        self.assertTrue((array(result) == array([3.0, 6.0, 9.0])).all())
        self.assertEqual(result.units, meters / second)
        result = 10 * a
        self.assertEqual(result.units, meters / second)
        result = a * 10
        self.assertTrue((array(result) == array([10, 20, 30])).all())
        self.assertEqual(result.units, meters / second)
        result = UnitScalar(3.0, units=second) * a
        self.assertTrue((array(result) == array([3.0, 6.0, 9.0])).all())
        self.assertEqual(result.units, meters)

    def test_multiply_units(self):
        a = UnitArray([1, 2, 3], units=meters)
        b = UnitArray([1, 2, 3], units=second)
        result = a * b
        self.assertEqual(result.units, meters * second)

    def test_pow_pass(self):
        a = UnitArray([1, 2, 3], units=meters)
        b = 0.5
        result = a**b
        self.assertEqual(result.units, meters**0.5)
        c = array(0.5)
        result = a**c
        self.assertEqual(result.units, meters**0.5)
        d = UnitArray(0.5, units=dimensionless)
        result = a**d
        self.assertEqual(result.units, meters**0.5)
        e = UnitArray([1, 2, 3], units=None)
        result = e ** 2
        self.assertEqual(result.units, None)

    def test_sqrt_no_pass(self):
        a = UnitArray([1.0, 2.0, 3.0], units=meters / second)
        result = sqrt(a)
        self.assertTrue(result.units is None)

    def test_sqrt_pass(self):
        a = UnitArray([1.0, 2.0, 3], units=dimensionless)
        result = sqrt(a)
        self.assertEqual(result.units, dimensionless)

    def test_le(self):
        a = UnitArray([1.0, 2.0, 3], units=dimensionless)
        b = UnitArray([3.0, 1.0, 1], units=2.0 * dimensionless)
        result = a <= b

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)
        c = 2.0
        result = b <= c
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], True)
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], True)

    def test_lt(self):
        a = UnitArray([1.0, 4.0, 3], units=dimensionless)
        b = UnitArray([3.0, 2.0, 1], units=2.0 * dimensionless)
        result = a < b

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], False)
        c = 3.0
        result = b < c
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], True)
        d = array([1.0, 2.0, 3.0])
        result = b < d
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)

    def test_ge(self):
        a = UnitArray([1.0, 4.0, 3], units=dimensionless)
        b = UnitArray([3.0, 2.0, 1], units=2.0 * dimensionless)
        result = a >= b

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], True)
        c = 2.0
        result = b >= c
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)
        d = array([1.0, 2.0, 3.0])
        result = b >= d
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)

    def test_gt(self):
        a = UnitArray([1.0, 4.0, 3], units=dimensionless)
        b = UnitArray([3.0, 2.0, 1], units=2.0 * dimensionless)
        result = a > b

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        c = 2.0
        result = b > c
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], False)
        d = array([1.0, 4.0, 3.0])
        result = b > d
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], False)

    def test_eq(self):
        a = UnitArray([1.0, 4.0, 3], units=dimensionless)
        b = UnitArray([3.0, 2.0, 1], units=2.0 * dimensionless)
        result = a == b

        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)
        c = 2.0
        result = b == c
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)
        d = array([1.0, 2.0, 3.0])
        result = b == d
        self.assertEqual(result[0], False)
        self.assertEqual(result[1], True)
        self.assertEqual(result[2], False)

    def test_ne(self):
        a = UnitArray([1.0, 4.0, 3], units=dimensionless)
        b = UnitArray([3.0, 2.0, 1], units=2.0 * dimensionless)
        result = a != b

        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
        c = 2.0
        result = b != c
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)

        d = array([1.0, 2.0, 3.0])
        result = b != d
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], False)
        self.assertEqual(result[2], True)
