""" Utilities around unit conversion and unit management.
"""
from six import string_types
import numpy as np

from scimath.units.api import convert, dimensionless, UnitArray, UnitScalar
from scimath.units.unit import InvalidConversion


def unit_scalars_almost_equal(x1, x2, eps=1e-9):
    """ Returns whether 2 UnitScalars are almost equal.

    Parameters
    ----------
    x1 : UnitScalar
        First unit scalar to compare.

    x2 : UnitScalar
        Second unit scalar to compare.

    eps : float
        Absolute precision of the comparison.
    """
    if not isinstance(x1, UnitScalar):
        msg = "x1 is supposed to be a UnitScalar but a {} was passed."
        msg = msg.format(type(x1))
        raise ValueError(msg)

    if not isinstance(x2, UnitScalar):
        msg = "x2 is supposed to be a UnitScalar but a {} was passed."
        msg = msg.format(type(x2))
        raise ValueError(msg)

    a1 = float(x1)
    try:
        a2 = convert(float(x2), from_unit=x2.units, to_unit=x1.units)
    except InvalidConversion:
        return False
    return np.abs(a1 - a2) < eps


def unit_arrays_almost_equal(uarr1, uarr2, eps=1e-9):
    """ Returns whether 2 UnitArrays are almost equal.

    Parameters
    ----------
    uarr1 : UnitArray
        First unit array to compare.

    uarr2 : UnitArray
        Second unit array to compare.

    eps : float
        Absolute precision of the comparison.
    """
    if not isinstance(uarr1, UnitArray):
        msg = "uarr1 is supposed to be a UnitArray but a {} was passed."
        msg = msg.format(type(uarr1))
        raise ValueError(msg)

    if not isinstance(uarr2, UnitArray):
        msg = "uarr2 is supposed to be a UnitArray but a {} was passed."
        msg = msg.format(type(uarr2))
        raise ValueError(msg)

    a1 = np.array(uarr1)
    try:
        a2 = convert(np.array(uarr2), from_unit=uarr2.units,
                     to_unit=uarr1.units)
    except InvalidConversion:
        return False
    return np.all(np.abs(a1 - a2) < eps)
