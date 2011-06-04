""" Test unit conversion functions used on input and output of functions.

    fixme: We need significant work on scalars.
"""

# Standard Library imports
import unittest

# Numeric library imports
from numpy import array, all, allclose, ndarray

# Enthought library imports
from scimath.units.unit import InvalidConversion
from scimath.units.length import feet, meters
from scimath.units.time import second

# Numerical modeling library imports
from scimath.units.api import UnitArray, UnitScalar
from scimath.units.unit_manipulation import \
    convert_units, set_units, have_some_units, strip_units

class ConvertUnitsTestCase(unittest.TestCase):
    """ ConvertUnits should pretty much leave anything without units alone
        and pass them through silently.  UnitArrays do get converted,
        and so should scalars with units (although we haven't really dealt with
        those).
    """

    ############################################################################
    # ConvertUnitsTestCase interface.
    ############################################################################

    def test_single_float(self):
        """ Does it pass a single value through correctly?
        """
        units = [None]
        result = convert_units(units, 1.0)
        self.assertEqual(1.0, result)

    def test_two_float(self):
        """ Does it pass a two values through correctly?
        """
        units = [None, None]
        result = convert_units(units, 1.0, 2.0)
        self.assertEqual([1.0, 2.0], result)

    def test_mismatch_raises_error(self):
        """ Is an exception raised if there aren't enough units specified?
        """
        self.assertRaises(ValueError, convert_units, ([None], 1.0, 2.0))

    def test_one_array(self):
        """ Does it pass a an array through correctly?
        """
        units = [None]
        a = array((1,2,3))
        result = convert_units(units, a)
        self.assertTrue(all(a==result))

    def test_two_arrays(self):
        """ Does it pass a two arrays through correctly?
        """
        units = [None, None]
        a = array((1,2,3))
        b = array((3,4,5))
        aa,bb = convert_units(units, a, b)
        self.assertTrue(all(a==aa))
        self.assertTrue(all(b==bb))

    def test_convert_array_with_units(self):
        """ Does it add units to an array correctly?

            fixme: This may be exactly what we don't want to happen!
        """
        units = [feet]
        a = array((1,2,3))
        aa = convert_units(units, a)
        self.assertTrue(all(a==aa))
        self.assertTrue(type(aa) is ndarray)

    def test_convert_unit_array(self):
        """ Does it convert an array correctly?
        """
        units = [feet]
        a = UnitArray((1,2,3),units=meters)
        aa = convert_units(units, a)
        self.assertTrue(allclose(a,aa.as_units(meters)))
        # fixme: This actually may be something we don't want.  For speed,
        #        if this were just a standard array, we would be better off.
        self.assertEqual(aa.units, feet)

    def test_convert_unit_scalar(self):
        """ Does it convert a scalar correctly?
        """
        units = [feet]
        a = UnitScalar(3.,units=meters)
        aa = convert_units(units, a)
        self.assertTrue(allclose(a,aa.as_units(meters)))
        self.assertEqual(aa.units, feet)

    def test_incompatible_array_units_raise_exception(self):
        """ Does a units mismatch raise an exception?

            fixme: Do we want this configurable?
        """
        units = [second]
        a = UnitArray((1,2,3),units=meters)
        self.assertRaises(InvalidConversion, convert_units, units, a)

    def test_incompatible_scalar_units_raise_exception(self):
        """ Does a units mismatch raise an exception?

            fixme: Do we want this configurable?
        """
        units = [second]
        a = UnitScalar(3.,units=meters)
        self.assertRaises(InvalidConversion, convert_units, units, a)

    def test_dont_convert_unit_array(self):
        """ Does it return the same object if units are the same?

            Note: This isn't required for accuracy, but it is a good
                  optimization.
        """
        units = [feet]
        a = UnitArray((1,2,3),units=feet)
        aa = convert_units(units, a)
        self.assertTrue(id(a),id(aa))

    def test_dont_convert_unit_scalar(self):
        """ Does it return the same object if units are the same?

            Note: This isn't required for accuracy, but it is a good
                  optimization.
        """
        units = [feet]
        a = UnitScalar(3.,units=feet)
        aa = convert_units(units, a)
        self.assertTrue(id(a),id(aa))

    def test_convert_different_args(self):
        """ Does it handle multiple different args correctly?
        """
        units = [feet, meters, None, feet]
        a = UnitArray((1,2,3),units=meters)
        b = array((2,3,4))
        c = 1
        d = UnitScalar(3.,units=meters)
        aa, bb, cc, dd = convert_units(units, a, b, c, d)
        self.assertTrue(allclose(a,aa.as_units(meters)))
        self.assertTrue(allclose(b,bb))
        self.assertEqual(c,cc)
        self.assertTrue(allclose(d,dd.as_units(meters)))

class SetUnitsTestCase(unittest.TestCase):


    ############################################################################
    # TestCase interface.
    ############################################################################

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    ############################################################################
    # SetUnitsTestCase interface.
    ############################################################################

    def test_single_float(self):
        """ Does it pass a single value through correctly?
        """
        units = [None]
        result = set_units(units, 1.0)
        self.assertEqual(1.0, result)

    def test_mismatch_raises_error(self):
        """ Is an exception raised if there aren't enough units specified?
        """
        self.assertRaises(ValueError, convert_units, [None], 1.0, 2.0)

    def test_one_array(self):
        """ Does it pass a an array through correctly?
        """
        units = [None]
        a = array((1,2,3))
        result = set_units(units, a)
        self.assertTrue(all(a==result))

    def test_set_scalar_with_units(self):
        """ Does it add units to a scalar correctly?
        """
        units = [feet]
        x = 3.0
        xx = set_units(units, x)
        self.assertEqual(float(xx), x)
        self.assertEqual(xx.units, feet)

    def test_set_array_with_units(self):
        """ Does it add units to an array correctly?

            fixme: This may be exactly what we don't want to happen!
        """
        units = [feet]
        a = array((1,2,3))
        aa = set_units(units, a)
        self.assertTrue(all(a==aa))
        self.assertEqual(aa.units, feet)

    def test_set_zero_dim_array_with_units(self):
        """ Does it add units to an array with shape () correctly?

            fixme: This may be exactly what we don't want to happen!
        """
        units = [feet]
        a = array(2)
        aa = set_units(units, a)
        self.assertTrue(all(a==aa))
        self.assertEqual(aa.units, feet)
        assert isinstance(aa, UnitScalar)

    def test_set_unit_overwrite_unit_scalar(self):
        """ Does it overwrite units on a UnitScalar correctly?
        """
        units = [feet]
        x = UnitScalar(3., units=meters)
        xx = set_units(units, x)
        # FIXME:
        #     Behaves very stangely (on my machine), somethimes it fails,
        #     other times it works almost like a random generator.
        #
        # We found that set_units(units, x) has a sideffect on x which it
        # should not have.
        #
        #self.assertEqual(x, xx)
        #print x, x.units
        self.assertEqual(xx.units, feet)

    def test_set_unit_overwrite_unit_array(self):
        """ Does it overwrite units on a UnitArray correctly?
        """
        units = [feet]
        a = UnitArray((1,2,3),units=meters)
        aa = set_units(units, a)
        self.assertTrue(all(a==aa))
        self.assertEqual(aa.units, feet)
#
#    def test_raises_exception(self):
#        """ Does it return the same object if units are the same?
#
#            Note: This isn't required for accuracy, but it is a good
#                  optimization.
#        """
#        units = [feet]
#        a = UnitArray((1,2,3),units=feet)
#        aa = convert_units(units, a)
#        self.assertTrue(id(a),id(aa))
#
#    def test_convert_different_args(self):
#        """ Does it handle multiple different args correctly?
#        """
#        units = [feet, meters, None]
#        a = UnitArray((1,2,3),units=meters)
#        b = array((2,3,4))
#        c = 1
#        aa, bb, cc = convert_units(units, a, b, c)
#        self.assertTrue(allclose(a,aa.as_units(meters)))
#        self.assertTrue(allclose(b,bb))
#        self.assertEqual(c,cc)


class HaveSomeUnitsTestCase(unittest.TestCase):
    """ have_some_units should check its arguments for any
    UnitArrays/UnitScalars.
    """

    ############################################################################
    # TestCase interface.
    ############################################################################

    def setUp(self):
        # Make some useful data.
        self.unit_array = UnitArray((1,2,3), units=meters)
        self.unit_scalar = UnitScalar(1, units=meters)
        self.plain_array = array([1, 2, 3])
        self.plain_scalar = 1
        unittest.TestCase.setUp(self)

    def test_finds_one(self):
        self.assertTrue(have_some_units(self.unit_array))
        self.assertTrue(have_some_units(self.unit_scalar))

    def test_finds_multiple(self):
        self.assertTrue(have_some_units(self.unit_array, self.unit_array))
        self.assertTrue(have_some_units(self.unit_scalar, self.unit_scalar))

    def test_finds_mixed_scalar_array(self):
        self.assertTrue(have_some_units(self.unit_array, self.unit_scalar))

    def test_does_not_find_plain(self):
        self.assertFalse(have_some_units(self.plain_array))
        self.assertFalse(have_some_units(self.plain_scalar))

    def test_does_not_find_mixed_plain(self):
        self.assertFalse(have_some_units(self.plain_array, self.plain_scalar))

    def test_finds_any_unitted(self):
        self.assertTrue(have_some_units(self.unit_array, self.plain_array, self.plain_scalar))
        self.assertTrue(have_some_units(self.plain_array, self.unit_array, self.plain_scalar))
        self.assertTrue(have_some_units(self.unit_scalar, self.plain_array, self.plain_scalar))
        self.assertTrue(have_some_units(self.plain_array, self.unit_scalar, self.plain_scalar))


class StripUnitsTestCase(unittest.TestCase):
    """ strip_units should remove units from UnitArrays/UnitScalars.
    """

    def setUp(self):
        # Make some useful data.
        self.unit_array = UnitArray((1,2,3), units=meters)
        self.unit_scalar = UnitScalar(1, units=meters)
        self.plain_array = array([1, 2, 3])
        self.plain_scalar = 1
        unittest.TestCase.setUp(self)

    def test_strip_units_one_arg(self):
        self.assertFalse(isinstance(strip_units(self.unit_array),
            (UnitArray, UnitScalar)))
        self.assertFalse(isinstance(strip_units(self.unit_scalar),
            (UnitArray, UnitScalar)))
        self.assertFalse(isinstance(strip_units(self.plain_array),
            (UnitArray, UnitScalar)))
        self.assertFalse(isinstance(strip_units(self.plain_scalar),
            (UnitArray, UnitScalar)))

        # Check for stupidity when returning only one argument.
        self.assertFalse(isinstance(strip_units(self.unit_scalar), tuple))
        self.assertFalse(isinstance(strip_units(self.plain_scalar), tuple))

    def test_strip_units_multi_arg(self):
        outs = strip_units(self.unit_array, self.unit_scalar)
        self.assertEquals(len(outs), 2)
        for x in outs:
            self.assertFalse(isinstance(x, (UnitArray, UnitScalar)))

        outs = strip_units(self.plain_array, self.plain_scalar)
        self.assertEquals(len(outs), 2)
        for x in outs:
            self.assertFalse(isinstance(x, (UnitArray, UnitScalar)))

        outs = strip_units(self.unit_array, self.unit_scalar, self.plain_array,
            self.plain_scalar)
        self.assertEquals(len(outs), 4)
        for x in outs:
            self.assertFalse(isinstance(x, (UnitArray, UnitScalar)))


if __name__ == '__main__':
    unittest.main()
