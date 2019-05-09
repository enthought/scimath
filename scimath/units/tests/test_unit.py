import unittest

from scimath.units.length import centimeter, meter
from scimath.units.unit import unit


class TestUnit(unittest.TestCase):
    def test_hashability_of_unit(self):
        unit_label_mapping = {
            meter: 'a meter',
            centimeter: 'a centimeter'
        }
        self.assertEqual(unit_label_mapping[meter], 'a meter')
        self.assertEqual(unit_label_mapping[centimeter], 'a centimeter')

    def test_units_should_hash_equal_if_they_compare_equal(self):
        meter = unit(1.0, (1, 0, 0, 0, 0, 0, 0))
        metre = unit(1.0, (1, 0, 0, 0, 0, 0, 0))
        self.assertEqual(meter, metre)
        self.assertEqual(hash(meter), hash(metre))
