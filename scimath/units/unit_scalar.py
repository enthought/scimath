from unit_array import UnitArray

# `array(x)` behaves like `x`, so we get unitted scalars for free. Efficiency
# is of course a concern, but there are no other solutions in sight, and this
# one hangs ridiculously low.
#
# TODO Profile!
#
class UnitScalar(UnitArray):
    ''' Scalars with units.

        >>> from scimath.units.length import cm
        >>> x = UnitScalar(5, units=cm)
        >>> x, x.units
        (UnitScalar(5, units='0.01*m+0.0'), 0.01*m+0.0)
        >>> x**2, (x**2).units
        (UnitScalar(25, units='0.0001*m**2+0.0'), 0.0001*m**2+0.0)
    '''
    def __repr__(self):
        return ("UnitScalar(%s, units='%s')" 
                % (self.item().__repr__(), repr(self.units)))
