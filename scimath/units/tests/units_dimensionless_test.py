from numpy.testing import assert_equal
from scimath.units.unit_scalar import UnitScalar
from scimath.units.unit import dimensionless

def dimensionless_test():
    """
    Test the modification to the division, multiplication and pow
    such that a dimensionless quantity formed by is indeed dimensionless
    """


    a = UnitScalar(1.0, units = 'm')
    b = UnitScalar(2.0, units = 'mm')
    d = UnitScalar(2.0, units = 'm**(-1)')

    c = a/b
    e = b*d

    f= UnitScalar(2.0, units = dimensionless)
    g = f**2

    assert_equal(c.units,dimensionless)
    assert_equal(e.units,dimensionless)
    assert_equal(g.units,dimensionless)

