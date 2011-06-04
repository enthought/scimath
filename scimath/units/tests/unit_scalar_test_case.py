import unittest

from enthought.testing.api import doctest_for_module
import enthought.units.unit_scalar as unit_scalar

class UnitScalarDocTestCase(doctest_for_module(unit_scalar)):
    pass

if __name__ == '__main__':
    import sys
    unittest.main(argv=sys.argv)
