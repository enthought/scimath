# Standard Library imports
import unittest

# Enthought Library imports
from traits.testing.api import doctest_for_module

# Numerical modeling library imports
from scimath.units import function_signature
from scimath.units.function_signature import (
    function_arguments, def_signature, call_signature,
)

class FunctionArgumentsDocTestCase(doctest_for_module(function_signature)):
    pass

class FunctionArgumentsTestCase(unittest.TestCase):

    ############################################################################
    # TestCase interface.
    ############################################################################

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    ############################################################################
    # FunctionArgumentsTestCase interface.
    ############################################################################

    def test_single(self):
        """ Does a function with a single positional argument work?
        """
        def func(value):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,('value',))
        self.assertEqual(kw,{})
        self.assertEqual(arg_ordered,('value',))

    def test_multiple(self):
        """ Does a function with multiple positional argument work?
        """
        def func(a,b,c):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,('a','b','c'))
        self.assertEqual(kw,{})
        self.assertEqual(arg_ordered,('a','b','c'))

    def test_single_kw(self):
        """ Does a function with a single keyword argument work?
        """
        def func(a=1):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,())
        self.assertEqual(kw,{'a':1})
        self.assertEqual(arg_ordered,('a',))

    def test_multiple_kw(self):
        """ Does a function with multiple keyword arguments work?
        """
        def func(a=1,b=2):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,())
        self.assertEqual(kw,{'a':1,'b':2})
        self.assertEqual(arg_ordered,('a','b'))

    def test_single_arg_and_kw(self):
        """ Does a function with one positional and one keyword arg work?
        """
        def func(a, b=1):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,('a',))
        self.assertEqual(kw,{'b':1})
        self.assertEqual(arg_ordered,('a','b'))

    def test_multiple_arg_and_kw(self):
        """ Does a function with two positional and two keyword arg work?
        """
        def func(a, b, c=1,d=2):
            pass
        args, kw, arg_ordered = function_arguments(func)
        self.assertEqual(args,('a','b'))
        self.assertEqual(kw,{'c':1,'d':2})
        self.assertEqual(arg_ordered,('a','b','c','d'))


class DefSignatureTestCase(unittest.TestCase):

    ############################################################################
    # TestCase interface.
    ############################################################################

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    ############################################################################
    # FunctionArgumentsTestCase interface.
    ############################################################################

    def test_kw(self):
        """ Does a function with a keyword and positional argument work?
        """
        def func(a,b=1):
            pass
        res = def_signature(func)
        self.assertEqual(res, 'def func(a, b=1):')

    def test_kw_with_list_argument(self):
        """ Does a function with a keyword argument as a list work?
        """
        def func(a,b=[]):
            pass
        res = def_signature(func)
        self.assertEqual(res, 'def func(a, b=[]):')

class CallSignatureTestCase(unittest.TestCase):

    ############################################################################
    # TestCase interface.
    ############################################################################

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)


    ############################################################################
    # FunctionArgumentsTestCase interface.
    ############################################################################

    def test_kw(self):
        """ Does a function with a keyword and positional argument work?
        """
        def func(a,b=1):
            pass
        res = call_signature(func)
        self.assertEqual(res, 'func(a, b)')

    def test_kw_with_list_argument(self):
        """ Does a function with a keyword argument as a list work?
        """
        def func(a,b=[]):
            pass
        res = call_signature(func)
        self.assertEqual(res, 'func(a, b)')


# Some functions to test on.
def just_args(x, y):
    pass

def just_kwds(y=1, x=2):
    pass

def args_and_kwds(x, z=1, y=2):
    pass


class FunctionSignatureTestCase(unittest.TestCase):

    def test_just_args(self):
        self.assertEquals(def_signature(just_args), "def just_args(x, y):")

    def test_just_kwds(self):
        self.assertEquals(def_signature(just_kwds), "def just_kwds(y=1, x=2):")

    def test_args_and_kwds(self):
        self.assertEquals(def_signature(args_and_kwds), "def args_and_kwds(x, z=1, y=2):")

if __name__ == '__main__':
    unittest.main()
