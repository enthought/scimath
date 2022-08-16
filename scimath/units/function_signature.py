# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Helper functions used in generating text for representing/calling python
    function objects.
"""

def function_arguments(func):
    """ Given a function, return its args, keywords, and full argument list.

        func is a function object.

        returns:
           args          Tuple of the non-keyword function arguments.
           kw            Dictionary of keyword arguments.
           args_ordered  Tuple of all arguments in their call order.
    """

    # Number of arguments to the function.
    arg_count = func.__code__.co_argcount

    # Names of the local variables in the function.
    var_names = func.__code__.co_varnames

    # The variables that come from the function inputs are at the from of the
    # local variable list.
    args_ordered = var_names[:arg_count]

    # Tuple of default values.  They are the values supplied to keyword
    # arguments and match to the last arguments in the
    # args_ordered list. It is None, if there are no keyword arguments.
    defaults = func.__defaults__

    if defaults is not None:
        # If there are keywords, then slice the variable list into
        # positional and keyword arguments.
        kw_count = len(defaults)
        args = args_ordered[:-kw_count]
        kw = dict(zip(args_ordered[-kw_count:], defaults))
    else:
        # If there are no keyword arguments, then everything is positional.
        args = args_ordered[:]
        kw = {}

    return args, kw, args_ordered


def def_signature(func, name=None):
    """ Return a string that duplicates the signature of func.

        func is a function object.  name is an optional string.  If it is
        specified, then name is used as the function name in the signature
        string.

        example:
            >>> def func(a,b): pass
            >>> def_signature(func)
            'def func(a, b):'
            >>> def_signature(func,name='foo')
            'def foo(a, b):'
    """

    if name is None:
        name = func.__name__

    args, kw, args_ordered = function_arguments(func)  # @UnusedVariable

    # Convert keyword args and their defaults into strings
    # fixme: This will go South in cases where the repr for
    # an object isn't an executable version of its constructor...
    # Make sure we iterate in the original order.
    kw_strings = ['%s=%r' % (k, kw[k]) for k in args_ordered[len(args):]]

    var_strings = list(args) + kw_strings
    var_string = ', '.join(var_strings)

    sig = "def %s(%s):" % (name, var_string)

    return sig


def call_signature(func, name=None):
    """ Return a string that is used to call a func.

        func is a function object.  name is an optional string.  If it is
        specified, then name is used as the function name in the call
        signature string.

        example:
            >>> def func(a,b=1): pass
            >>> call_signature(func)
            'func(a, b)'
            >>> call_signature(func,name='foo')
            'foo(a, b)'
    """
    if name is None:
        name = func.__name__

    args, kw, args_ordered = function_arguments(func)  # @UnusedVariable

    var_string = ', '.join(args_ordered)

    sig = "%s(%s)" % (name, var_string)

    return sig

if __name__ == "__main__":
    import doctest
    doctest.testmod()
