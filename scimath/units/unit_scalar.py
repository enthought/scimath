# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from .unit_array import UnitArray

# `array(x)` behaves like `x`, so we get unitted scalars for free. Efficiency
# is of course a concern, but there are no other solutions in sight, and this
# one hangs ridiculously low.
#
# TODO Profile!
#


class UnitScalar(UnitArray):
    """ Scalars with units.

        >>> from scimath.units.length import cm
        >>> x = UnitScalar(5, units=cm)
        >>> x, x.units
        (UnitScalar(5, units='0.01*m'), 0.01*m)
        >>> x**2, (x**2).units
        (UnitScalar(25, units='0.0001*m**2'), 0.0001*m**2)
    """
    def __repr__(self):
        s = "{klass}({val}, units='{unit}')"
        str_val = self.item().__repr__()
        klass = type(self).__name__
        return s.format(klass=klass, val=str_val, unit=repr(self.units))

    def __str__(self):
        s = "{klass} ({unit}): {val}"
        str_val = self.item().__str__()
        if self.units.label is not None:
            str_unit = self.units.label
        else:
            str_unit = repr(self.units)

        return s.format(klass=type(self).__name__, val=str_val, unit=str_unit)
