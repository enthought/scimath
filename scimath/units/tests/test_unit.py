import unittest

from scimath.units.length import centimeter, meter


class TestUnit(unittest.TestCase):
    def test_hashability_of_unit(self):
        unit_label_mapping = {
            meter: 'a meter',
            centimeter: 'a centimerer'
        }
        self.assertTrue(unit_label_mapping[meter], 'a meter')
        self.assertTrue(unit_label_mapping[centimeter], 'a centimeter')
