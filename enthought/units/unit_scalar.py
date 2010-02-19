from unit_array import UnitArray

# `array(x)` behaves like `x`, so we get unitted scalars for free. Efficiency
# is of course a concern, but there are no other solutions in sight, and this
# one hangs ridiculously low.
#
# TODO Profile!
#
class UnitScalar(UnitArray):
    ''' Scalars with units.

        >>> from enthought.units.length import cm
        >>> x = UnitScalar(5, units=cm)
        >>> x, x.units
        (UnitScalar(5), 0.01*m)
        >>> x**2, (x**2).units
        (UnitScalar(25), 0.01*m)
    '''
    def __repr__(self):
        return "UnitScalar(%s, units='%s')" % (str(self), repr(self.units))
