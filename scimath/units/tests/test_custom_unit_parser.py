# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Tests for customizing the unit parser.
"""
import unittest

from scimath.units.api import unit_parser
from scimath.units.unit_parser import UnableToParseUnits
from scimath.units.tests import sample_units


class TestCustomUnitParser(unittest.TestCase):

    def test_extend_from_module(self):
        # Custom unit is not known initially
        with self.assertRaises(UnableToParseUnits):
            unit_parser.parse_unit("custom_unit", suppress_unknown=False)

        unit_parser.parser.extend(sample_units)

        # Once parser is extended, the unit can be parsed
        expected_unit = sample_units.custom_unit
        self.assertEqual(unit_parser.parse_unit("custom_unit"), expected_unit)
        self.assertEqual(unit_parser.parse_unit("cuwl"), expected_unit)
