# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""Utility functions for physical quantities
"""

# Global module imports
from copy import copy


def dict_mul(a, n):
    """Given a dictionary, multiply values by a scalar

    Parameters
    ----------
        a: dict
            the dictionary to be multiplied.
        n: float
            the scalar to multiply by

    Example
    -------
    Given a dictionary and scalar:

    >>> a = {'a': 2.0, 'b': -4.0}
    >>> n = 1.5
    >>> dict_mul(a, n)
    {'a': 3.0, 'b': -6.0}

    """
    if n == 0:
        return {}
    c = copy(a)
    for key in c:
        c[key] *= n
    return c


def dict_div(a, n):
    """Given a dictionary, divide values by a scalar

    Parameters
    ----------
        a: dict
            the dictionary to be divided.
        n: float
            the scalar to divide by

    Example
    -------
    Given a dictionary and scalar:

    >>> a = {'a': 2.0, 'b': -4.0}
    >>> n = 0.5
    >>> dict_div(a, n)
    {'a': 4.0, 'b': -8.0}

    """
    c = copy(a)
    for key in c:
        c[key] /= n
    return c


def dict_add(a, b):
    """Given two dictionaries, add values by key, removing zero entries

    Parameters
    ----------
        a, b : dict
            the dictionaries to be added.

    Example
    -------
    Given two dictionaries:

    >>> a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
    >>> b = {'a': 1.5, 'c': 12.0, 'd': -2.0}
    >>> dict_add(a, b)
    {'a': 4.5, 'b': -4.0, 'c': 12.0}
    """
    c = copy(b)
    for key, value in a.items():
        c[key] = value + b.get(key, 0)
        if c[key] == 0.0:
            del c[key]
    return c


def dict_sub(a, b):
    """Given two dictionaries, subtract values by key, removing zero entries

    Parameters
    ----------
    a, b : dict
        the dictionaries to be added.

    Example
    -------
    Given two dictionaries::

        >>> a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
        >>> b = {'a': 1.5, 'c': 12.0, 'd': 2.0}
        >>> dict_sub(a, b)
        {'a': 1.5, 'b': -4.0, 'c': -12.0}
    """
    c = copy(a)
    for key, value in b.items():
        c[key] = a.get(key, 0) - value
        if c[key] == 0.0:
            del c[key]
    return c


def python_powers(key, value):
    """ Convert a value to a power expressed in standard Python syntax

    Parameters
    ----------
    value : number
        the value we want to convert to a power

    Result
    ------
    s : string
        a string representing the power
    """
    if value == 1:
        return key
    else:
        return key + "**" + str(value).rstrip(".0")

_unicode_supers = {
    "0": u"\u2070",
    "1": u"\u00B9",
    "2": u"\u00B2",
    "3": u"\u00B3",
    "4": u"\u2074",
    "5": u"\u2075",
    "6": u"\u2076",
    "7": u"\u2077",
    "8": u"\u2078",
    "9": u"\u2079",
    "+": u"\u207A",
    "-": u"\u207B",
}

_unicode_supers_reversed = dict((value, key) for key, value in
                                _unicode_supers.items())


def unicode_powers(key, value):
    """ Convert a value to a power using unicode superscripts

    Parameters
    ----------
    value : number
        the value we want to convert to a power

    Result
    ------
    s : unicode
        a unicode string representing the power
    """
    if value == 1:
        return key
    else:
        s = str(value).rstrip(".0")
        try:
            return key + u"".join(_unicode_supers[char] for char in s)
        except KeyError:
            # don't know how to handle, so punt - most likely reason is
            # a decimal point in the expression
            return key + u"^" + s


def tex_powers(key, value):
    """ Convert a value to a power expression in TeX/LaTeX

    Parameters
    ----------
    value : number
        the value we want to convert to a power

    Result
    ------
    s : str
        a TeX/LaTeX string representing the power
    """
    if value == 1:
        return key
    else:
        return key + "^{" + str(value).rstrip(".0") + "}"

_named_powers = {
    2: "square",
    3: "cubic",
    4: "quartic",
    5: "quintic",
}


def name_powers(key, value):
    """ Convert a value to a power expression in English

    Parameters
    ----------
    value : number
        the value we want to convert to a power

    Result
    ------
    s : str
        a string representing the power
    """
    if value == 1:
        return key
    elif value in _named_powers:
        return _named_powers[value] + " " + key
    else:
        return key + " to the " + str(value).rstrip(".0")


def format_expansion(dimensions, mul="*", pow_func=python_powers, div=False,
                     empty_numerator="1", div_symbol="/", group_symbols="()"):
    """ Format a dictionary of symbol, power pairs """
    if div:
        numerator = mul.join(pow_func(key, value)
                             for key, value in sorted(dimensions.items())
                             if value > 0)
        if numerator == "":
            numerator = empty_numerator
        denominator_terms = [pow_func(key, -value)
                             for key, value in sorted(dimensions.items())
                             if value < 0]
        if len(denominator_terms) > 1:
            return numerator + div_symbol + group_symbols[0] + \
                mul.join(denominator_terms) + group_symbols[1]
        elif len(denominator_terms) == 1:
            return numerator + div_symbol + denominator_terms[0]
        else:
            return numerator
    else:
        return mul.join(pow_func(key, value)
                        for key, value in sorted(dimensions.items())
                        if value != 0)
