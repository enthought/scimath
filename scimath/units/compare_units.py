""" Utilities around unit comparisons.
"""
import numpy as np

from scimath.units.api import convert, UnitArray, UnitScalar
from scimath.units.unit import InvalidConversion


def unit_scalars_almost_equal(x1, x2, rtol=1e-9):
    """ Returns whether 2 UnitScalars are almost equal.

    More precisely, what is tested is whether abs(a1-a2) < rtol*abs(a2), where
    a1=float(x1) and a2=float(x2) after conversion to x1's units.

    Parameters
    ----------
    x1 : UnitScalar
        First unit scalar to compare.

    x2 : UnitScalar
        Second unit scalar to compare.

    rtol : float
        Relative precision of the comparison.
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
    return np.abs(a1 - a2) < np.abs(rtol * a2)


def unit_arrays_almost_equal(uarr1, uarr2, rtol=1e-9):
    """ Returns whether 2 UnitArrays are almost equal (must be the same shape).

    More precisely, what is tested is whether abs(a1-a2) < rtol*abs(a2) for all
    values in the arrays, once uarr2 has been converted to uarr1's units.

    Parameters
    ----------
    uarr1 : UnitArray
        First unit array to compare.

    uarr2 : UnitArray
        Second unit array to compare.

    rtol : float
        Relative precision of the comparison.
    """
    if not isinstance(uarr1, UnitArray):
        msg = "uarr1 is supposed to be a UnitArray but a {} was passed."
        msg = msg.format(type(uarr1))
        raise ValueError(msg)

    if not isinstance(uarr2, UnitArray):
        msg = "uarr2 is supposed to be a UnitArray but a {} was passed."
        msg = msg.format(type(uarr2))
        raise ValueError(msg)

    if uarr1.shape != uarr2.shape:
        return False

    a1 = np.array(uarr1)
    try:
        a2 = convert(np.array(uarr2), from_unit=uarr2.units,
                     to_unit=uarr1.units)
    except InvalidConversion:
        return False

    return np.all(np.abs(a1 - a2) < np.abs(rtol * a2))
