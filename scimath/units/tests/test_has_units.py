# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Standard Library imports
import unittest

# Numeric library imports
import numpy
from numpy import arange, allclose, array, all  # @UnresolvedImport
from numpy.testing import assert_array_almost_equal

# Enthought library imports
from traits.testing.api import doctest_for_module
from scimath.units.length import feet, meters
from scimath.units.time import second
from scimath.units.unit_parser import unit_parser

# Numerical modeling library imports
import scimath.units.has_units as has_units_
from scimath.units.api import has_units, UnitArray, UnitScalar


class HasUnitsDocTestCase(doctest_for_module(has_units_)):
    pass


class HasUnitsTestCase(unittest.TestCase):

    ##########################################################################
    # TestCase interface.
    ##########################################################################

    def assertEqual(self, first, second, msg=None):
        """Fail if the two objects are unequal as determined by the '=='
           operator.

           We've overloaded this here to handle arrays.
        """
        if not all(first == second):
            raise self.failureException(msg or '%r != %r' % (first, second))

    ##########################################################################
    # HasUnitsTestCase interface.
    ##########################################################################

    def test_wrapped_behaves_like_unwrapped(self):
        """ Does wrapped function behave like non-wrapped function.

        """
        def func(value):
            return value

        decorater = has_units()
        func_wrapped = decorater(func)

        self.assertEqual(func(1), func_wrapped(1))

    def test_wrapped_with_input_units(self):
        """ Does wrapped function with inputs behave like non-wrapped function?

        """

        def func(value):
            return value

        decorater = has_units(inputs="value: a value: units=m/s;")
        func_wrapped = decorater(func)

        self.assertEqual(func(1), func_wrapped(1))

    def test_wrapped_with_output_units(self):
        """ Does wrapped function with outputs behave like non-wrapped function?

        """

        def func(value):
            return value

        decorater = has_units(outputs="value: a value: units=m/s;")
        func_wrapped = decorater(func)

        arg = array((1, 2, 3))
        std = func(arg)
        actual = func_wrapped(arg)
        self.assertEqual(std, actual)

    def test_wrapped_with_two_output_units(self):
        """ Are two outputs handled correctly?

        """

        def func(v1, v2):
            return v1, v2

        decorater = has_units(outputs="""v1: a value: units=m/s;
                                        v2: another value: units=ft/s;
                                     """)
        func_wrapped = decorater(func)

        arg = array((1, 2, 3))
        std_v1, std_v2 = func(arg, arg + 1)
        actual_v1, actual_v2 = func_wrapped(arg, arg + 1)
        self.assertEqual(std_v1, actual_v1)
        self.assertEqual(std_v2, actual_v2)

    def test_wrapped_with_units_decorated(self):

        def func(value):
            return value

        @has_units(inputs="value: a value: units=m/s;")
        def func_wrapped(value):
            return value

        self.assertEqual(func(1), func_wrapped(1))

    def test_unit_array_with_units_decorated(self):

        def func(value):
            return value

        @has_units(inputs="value: a value: units=m/s;")
        def func_wrapped(value):
            return value

        a = UnitArray(arange(100), units=meters / second)
        self.assertTrue(allclose(func(a).as_units(meters / second),
                                 func_wrapped(a)))

        a = UnitArray(arange(100), units=feet / second)
        self.assertTrue(allclose(func(a).as_units(meters / second),
                                 func_wrapped(a)))

    def test_unit_array_with_decorated_docstring_function(self):
        """Does has_units wrap with docstring work ?
        """

        def addfunc(a, b):
            return a + b

        @has_units
        def add(a, b):
            ''' Add two arrays in ft/s and convert them to m/s.

            Parameters
            ----------
            a : array : units=ft/s
                An array
            b : array : units=ft/s
                Another array

            Returns
            -------
            c : array : units=m/s
                c = a + b
            '''
            return (a + b) * 0.3048

        a = UnitArray(arange(100), units=feet / second)
        b = UnitArray(arange(100)**2, units=feet / second)
        self.assertTrue(allclose(addfunc(a, b).as_units(meters / second),
                                 add(a, b)))

        a = UnitArray(arange(100), units=meters / second)
        b = UnitArray(arange(100)**2, units=meters / second)
        self.assertTrue(allclose(addfunc(a, b).as_units(meters / second),
                                 add(a, b)))

    def test_unit_array_with_decorated_docstring_and_inputted_parameters(self):
        """Does has_units wrap with expanded docstring and inputting
        parameters work the same ?
        """

        @has_units(inputs="a:an array:units=ft/s;b:array:units=ft/s",
                   outputs="c:an array:units=m/s")
        def add(a, b):
            " Add two arrays in ft/s and convert them to m/s. "
            return (a + b) * 0.3048

        @has_units
        def add_doc(a, b):
            ''' Add two arrays in ft/s and convert them to m/s.

            Parameters
            ----------
            a : array : units=ft/s
                An array
            b : array : units=ft/s
                Another array

            Returns
            -------
            c : array : units=m/s
                c = a + b
            '''
            return (a + b) * 0.3048

        a = UnitArray(arange(100), units=feet / second)
        b = UnitArray(arange(100)**2, units=feet / second)
        self.assertTrue(allclose(add_doc(a, b),
                                 add(a, b)))

        a = UnitArray(arange(100), units=meters / second)
        b = UnitArray(arange(100)**2, units=meters / second)
        self.assertTrue(allclose(add_doc(a, b),
                                 add(a, b)))

    def test_wrapped_adds_summary(self):
        """ Is summary information added correctly?
        """
        summary = "a function"

        @has_units(summary=summary)
        def func(value):
            return value

        self.assertTrue(func.summary == summary)

    def test_wrapped_adds_doc(self):
        """ Is doc information added correctly?
        """
        doc = "documentation about the function"

        @has_units(doc=doc)
        def func(value):
            return value

        self.assertTrue(func.doc == doc)

    def test_wrapped_adds_inputs(self):
        """ Are input specifications added correctly?
        """

        @has_units(inputs="v1:a value:units=m/s")
        def func(v1, v2):
            return v1 + v2

        self.assertTrue(len(func.inputs) == 2)

        # Does the 1st variable have its name and units assigned correctly?
        self.assertTrue(func.inputs[0].name == 'v1')
        self.assertTrue(func.inputs[0].units == unit_parser.parse_unit('m/s'))

        # Was the 2nd (unspecified) input given an input variable?
        self.assertTrue(func.inputs[1].name == 'v2')
        self.assertTrue(func.inputs[1].units is None)

    def test_wrapped_adds_outputs(self):
        """ Are output specifications added correctly?
        """

        @has_units()
        def func(v1, v2):
            return v1 + v2

        self.assertTrue(len(func.outputs) == 1)

        # Does the output have its name and units assigned correctly?
        self.assertTrue(func.outputs[0].name == 'result')
        self.assertTrue(func.outputs[0].units is None)

    def test_wrapped_adds_outputs2(self):
        """ Are output specifications added correctly?
        """

        @has_units(outputs="out: out desc:units=m/s")
        def func(v1, v2):
            return v1 + v2

        self.assertTrue(len(func.outputs) == 1)

        # Does the output have its name and units assigned correctly?
        self.assertTrue(func.outputs[0].name == 'out')
        self.assertTrue(func.outputs[0].units == unit_parser.parse_unit('m/s'))


# Some functions to play with.
def foo(x, y):
    """ Foo

    Parameters
    ----------
    x : scalar : units=m
        X
    y : scalar : units=s
        Y

    Returns
    -------
    z : scalar : units=m/s
    """
    assert not isinstance(x, (UnitArray, UnitScalar))
    assert not isinstance(y, (UnitArray, UnitScalar))
    z = x / y
    return z

foo_with_units = has_units(foo)


def bar(x, y):
    """ Bar

    Parameters
    ----------
    x : scalar : units=m
        X
    y : scalar : units=s
        Y

    Returns
    -------
    z : scalar : units=m
    """

    if y > 1:
        z = x - x
    else:
        z = x + x
    return z


vec_bar_with_units = has_units(numpy.vectorize(bar))


class HasUnitsDecoratorTestCase(unittest.TestCase):

    def setUp(self):
        # Make some data to play with.
        self.meter_array = UnitArray([1., 2, 3], units=meters)
        self.second_array = UnitArray([3., 2, 1], units=second)
        self.feet_array = UnitArray([4., 5, 6], units=feet)
        self.meter_scalar = UnitScalar(1., units=meters)
        self.second_scalar = UnitScalar(3., units=second)
        self.feet_scalar = UnitScalar(4., units=feet)

    def test_decorator_plays_nice(self):
        self.assertEqual(foo_with_units.__module__, foo.__module__)
        self.assertEqual(foo_with_units.__doc__, foo.__doc__)
        self.assertEqual(foo_with_units.__name__, foo.__name__)

    def test_input_variables_parsed(self):
        inputs = foo_with_units.inputs
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs[0].name, 'x')
        self.assertEqual(inputs[0].units, meters)
        self.assertEqual(inputs[1].name, 'y')
        self.assertEqual(inputs[1].units, second)

    def test_output_variables_parsed(self):
        outputs = foo_with_units.outputs
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].name, 'z')
        self.assertEqual(outputs[0].units, meters / second)

    def test_no_internal_units_array(self):
        z = foo_with_units(self.meter_array, self.second_array)
        self.assertTrue(isinstance(z, UnitArray))
        self.assertEqual(z.units, meters / second)

    def test_no_internal_units_scalar(self):
        z = foo_with_units(self.meter_scalar, self.second_scalar)
        self.assertTrue(isinstance(z, UnitScalar))
        self.assertEqual(z.units, meters / second)

    def test_feet(self):
        z = foo_with_units(self.feet_array, self.second_array)
        self.assertTrue(isinstance(z, UnitArray))
        self.assertEqual(z.units, meters / second)
        assert_array_almost_equal(z, numpy.array([0.4064, 0.762, 1.8288]))
        z = foo_with_units(self.feet_scalar, self.second_scalar)
        self.assertTrue(isinstance(z, UnitScalar))
        self.assertEqual(z.units, meters / second)
        assert_array_almost_equal(z, 0.4064)

    def test_v_decorator_plays_nice(self):
        self.assertEqual(vec_bar_with_units.__module__, bar.__module__)
        self.assertEqual(vec_bar_with_units.__doc__, bar.__doc__)
        self.assertEqual(vec_bar_with_units.__name__, bar.__name__)

    def test_v_input_variables_parsed(self):
        inputs = vec_bar_with_units.inputs
        self.assertEqual(len(inputs), 2)
        self.assertEqual(inputs[0].name, 'x')
        self.assertEqual(inputs[0].units, meters)
        self.assertEqual(inputs[1].name, 'y')
        self.assertEqual(inputs[1].units, second)

    def test_v_output_variables_parsed(self):
        outputs = vec_bar_with_units.outputs
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0].name, 'z')
        self.assertEqual(outputs[0].units, meters)

    def test_v_no_internal_units_array(self):
        z = vec_bar_with_units(self.meter_array, self.second_array)
        self.assertTrue(isinstance(z, UnitArray))
        self.assertEqual(z.units, meters)

    def test_v_no_internal_units_scalar(self):
        z = vec_bar_with_units(self.meter_scalar, self.second_scalar)
        self.assertTrue(isinstance(z, UnitScalar))
        self.assertEqual(z.units, meters)

    def test_v_feet(self):
        z = vec_bar_with_units(self.feet_array, self.second_array)
        self.assertTrue(isinstance(z, UnitArray))
        self.assertEqual(z.units, meters)
        assert_array_almost_equal(z, numpy.array([0.0, 0.0, 3.6576]))
        z = vec_bar_with_units(self.feet_scalar, self.second_scalar)
        self.assertTrue(isinstance(z, UnitScalar))
        self.assertEqual(z.units, meters)
        assert_array_almost_equal(z, 0.0)
