""" Tests for customizing the unit parser.
"""
import unittest

from scimath.units.api import unit_parser
from scimath.units.length import mm
from scimath.units.unit_parser import UnableToParseUnits
import sample_units



class TestCustomUnitParser(unittest.TestCase):

    def test_extend_from_module(self):
        # Custom units are not known initially
        with self.assertRaises(UnableToParseUnits):
            unit_parser.parse_unit("cuwl", suppress_unknown=False)
        with self.assertRaises(UnableToParseUnits):
            unit_parser.parse_unit("custom_unit", suppress_unknown=False)

        unit_parser.parser.extend(sample_units)
        self.assertEqual(unit_parser.parse_unit("cuwl"), mm)
        self.assertEqual(unit_parser.parse_unit("custom_unit"), mm)
