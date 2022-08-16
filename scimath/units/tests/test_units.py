# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Very basic 'unit' unit tests.
"""

#############################################################################
# Imports:
#############################################################################
# Standard library imports
import unittest
import logging

# Major package imports
import numpy

# Local units imports
import scimath.units as units
from scimath.units.api import convert_str
from scimath.units.unit import unit
from scimath.units.mass import kg, metric_ton
from scimath.units.temperature import kelvin, celsius, fahrenheit
from scimath.units import SI, acceleration, angle, area, density, \
    electromagnetism, frequency, geo_units, length, speed, temperature, \
    time, volume
from scimath.units.quantity import Quantity
from scimath.units.style_manager import style_manager
from scimath.units.unit_manager import unit_manager
from scimath.units.smart_unit import is_dimensionless

from scimath.units.speed import meters_per_second

from scimath.units.unit_parser import UnableToParseUnits, unit_parser


logger = logging.getLogger(__name__)


#############################################################################
# Assignment:
#############################################################################

ms2 = acceleration.meters_per_second_squared
fs2 = acceleration.feet_per_second_squared

mass = 1000
acc = 9.8
acc_imp = 32.152231

converters = unit_manager.unit_converters
systems = unit_manager.unit_systems
test_data = numpy.arange(1, 100, .10)

#############################################################################
# Tests:
#############################################################################


class test_units(unittest.TestCase):

    def test_with_si(self):
        f = self._compute_force(mass, acc)
        self.assertEqual(f, mass * acc)

    def test_with_ton(self):
        f = self._compute_force(mass / 1000, acc, mass_units=metric_ton)
        self.assertEqual(f, mass * acc)

    def test_with_imp(self):
        f = self._compute_force(mass, acc_imp, acc_units=fs2)
        self.assertAlmostEqual(f, mass * acc, 4)

    def test_temperature(self):
        k = 200
        c = -73.15
        f = -99.67
        k2c = units.convert(k, kelvin, celsius)
        self.assertAlmostEqual(k2c, c)
        k2f = units.convert(k, kelvin, fahrenheit)
        self.assertAlmostEqual(k2f, f)
        f2c = units.convert(f, fahrenheit, celsius)
        self.assertAlmostEqual(f2c, c)
        t1 = units.convert(-40.0, temperature.fahrenheit, temperature.celsius)
        self.assertAlmostEqual(t1, -40.0, 6)
        t2 = units.convert(0.0, temperature.celsius, temperature.fahrenheit)
        self.assertAlmostEqual(t2, 32.0, 6)

    def test_area(self):
        self.assertEqual(1 * area.square_mile / (640 * area.acre), 1.0)

    def test_density(self):
        d1 = units.convert(1, density.lb_per_gal,
                           density.grams_per_cubic_centimeter)
        self.assertAlmostEqual(d1, 0.1198284429, 6)

    def test_frequency(self):
        f1 = units.convert(1, frequency.hertz, frequency.khz)
        self.assertAlmostEqual(f1, 0.001, 6)

    def test_speed(self):
        s1 = units.convert(55, speed.miles_per_hour, speed.meters_per_second)
        self.assertAlmostEqual(s1, 24.5872, 6)

    def test_unit_db(self):

        from scimath.units import unit_db
        udb = unit_db.UnitDB()
        udb.get_family_members_from_file()
        udb.get_unit_families_from_file()
        # spot check reading default data into db object
        self.assertEqual(udb.get_family_name("dt"), 'psonic')

    def test_style_manager(self):

        test_quantity = Quantity(
            test_data,
            name="vp",
            units='m/s',
            family_name="pvelocity")

        self.assertEqual(
            style_manager.get_info(
                test_quantity,
                'line'),
            'solid')
        self.assertEqual(
            style_manager.get_info(
                test_quantity,
                'color'),
            'black')

    def test_style_manager_ranges(self):

        test_quantity = Quantity(
            test_data,
            name="vp",
            units='m/s',
            family_name="pvelocity")

        # unit_system optional, since kgs is default
        self.assertEqual(style_manager.get_range(test_quantity, unit_system='kgs'),
                         (1.5, 6.5))
        self.assertEqual(style_manager.get_range(test_quantity.invert(), unit_system='kgs'),
                         (500.0, 0.0))

    def test_conversion_tracks_parents(self):
        """ Test that a _converted_from traits is set appropriately.

        Quantity converted from another quantity via change_unit_system has
        the _converted_from trait set appropriately.
        """

        metric_system = unit_manager.get_unit_system('METRIC')
        metric_depth = metric_system.units('depth')

        q1 = Quantity(32, units='m', family_name='depth')
        q2 = q1.change_unit_system('IMPERIAL')
        q3 = q2.change_unit_system('METRIC')

        self.assertEqual(q1, q2._converted_from,
                         "Conversion failed to track conversion parent.")
        self.assertEqual(q2, q3._converted_from,
                         "Conversion failed to track conversion parent.")

    def test_propagation_base(self):
        """ Tests that propagation works for an original quantity. """

        q1 = Quantity(10, units='m', family_name='depth')
        q1.propagate_data_changes()

        self.assertEqual(10, q1.data,
                         "Propagation modified the base data.")

    def test_propagation(self):
        """ Tests data propagation for a single converted quantity. """

        q1 = Quantity(10, units='m', family_name='depth')
        q2 = q1.change_unit_system('IMPERIAL')
        q3 = q1.change_unit_system('METRIC')

        q2.data = 2 * q2.data
        q2.propagate_data_changes()

        self.assertAlmostEqual(20., q1.data, 1,
                               "Propagation test expected data 20, got %s" % str(q1.data))

        q3.data = 3 * q3.data
        q3.propagate_data_changes()

        self.assertAlmostEqual(30., q1.data, 1,
                               "Propagation test expected data 30, got %s" % str(q1.data))

    def test_get_original(self):

        q1 = Quantity(10, units='m', family_name='depth')
        q2 = q1.change_unit_system('IMPERIAL')
        q3 = q1.change_unit_system('METRIC')

        self.assertEqual(q1, q1.get_original(),
                         "Original quantity's get_original method failed to return self.")
        self.assertEqual(q1, q2.get_original(),
                         "First child get_original failed to return original.")
        self.assertEqual(q1, q3.get_original(),
                         "Second child get_original failed to return original.")

    def test_unit_parser_dimensionless(self):
        for label in ['', 'None', 'none', 'unknown', 'unitless']:
            dless = unit_parser.parse_unit(label, suppress_unknown=False)
            self.assertTrue(is_dimensionless(dless))
            self.assertEqual(dless.value, 1)

    def test_unit_parser_caps(self):
        mpers_in_caps = Quantity(1.0, units="M/S", family_name="pvelocity")
        self.assertEqual(mpers_in_caps.units.derivation, meters_per_second.derivation,
                         "Capitalized units rejected")

    def test_unit_parser_only_units(self):
        for bad_name in ['copy', 'math', '__id__', '__doc__', '__builtin__',
                         'Exception']:
            self.assertRaises(
                UnableToParseUnits,
                unit_parser.parse_unit, bad_name, suppress_unknown=False,
            )
        # But plain numbers like the SI prefixes are kept.
        for good_name in ['hecto', 'yotta']:
            self.assertTrue(is_dimensionless(
                unit_parser.parse_unit(good_name, suppress_unknown=False)))

    def test_unit_parser_derivation_valid(self):
        # Make sure every derivation of the SI core units can be parsed.
        for i, label in enumerate(unit._labels):
            derivation = [0] * len(unit._labels)
            derivation[i] = 1
            base_unit = unit(1.0, tuple(derivation))
            base_unit.label = label
            self.assertEqual(
                unit_parser.parse_unit(label, suppress_unknown=False),
                base_unit,
            )
        self.assertEqual(
            unit_parser.parse_unit('S', suppress_unknown=False),
            SI.siemens,
        )

    def test_unit_parser_non_python(self):
        parse = lambda s: unit_parser.parse_unit(s, suppress_unknown=False)
        odd_units = [
            angle.circle,
            angle.grad,
            angle.minutes,
            acceleration.m_per_s2,
            electromagnetism.mf,
            volume.cm3,
        ]
        for u in odd_units:
            self.assertEqual(parse(u.label), u)

    def test_unit_parser_offsets(self):
        parse = lambda s: unit_parser.parse_unit(s, suppress_unknown=False)
        offset_units = [
            temperature.degC,
            temperature.degF,
        ]
        for u in offset_units:
            self.assertEqual(parse(repr(u)), u)

    def test_family_compatibility(self):
        """ test are_compatible_families """

        self.assertTrue(unit_manager.are_compatible_families('none', 'pvelocity'))
        self.assertTrue(unit_manager.are_compatible_families('none', 'foo'))
        self.assertTrue(unit_manager.are_compatible_families('foo', 'foo'))
        self.assertTrue(not unit_manager.are_compatible_families('bar', 'foo'))
        self.assertTrue(not unit_manager.are_compatible_families('bar', 'none'))

    def test_get_inverse(self):
        """ test get_inverse_family_name and get_inverse_name """

        # Try with family_names provided
        self.assertEqual(
            unit_manager.get_inverse_family_name('psonic'),
            'pvelocity')
        self.assertEqual(unit_manager.get_inverse_name('psonic'), 'vp')
        # Now try with family_members provided
        self.assertEqual(
            unit_manager.get_inverse_family_name('dt'),
            'pvelocity')
        self.assertEqual(unit_manager.get_inverse_name('dt'), 'vp')

    def test_unit_equal(self):
        """ test unit class __eq__ method"""
        um1 = length.m
        um2 = length.m
        uft = length.feet

        self.assertTrue(um1 == um2)
        self.assertTrue(not(um1 == uft))

    def test_unit_notequal(self):
        """ test unit class __ne__ method"""
        um1 = length.m
        um2 = length.m
        uft = length.feet

        self.assertTrue(not(um1 != um2))
        self.assertTrue(um1 != uft)

    def test_smart_unit_equal(self):
        """ test smart unit class __eq__ method"""
        qm1 = Quantity(1, units='m', family_name='depth')
        qm2 = Quantity(2, units='m', family_name='depth')
        qft = Quantity(1, units='feet', family_name='depth')

        self.assertTrue(qm1.units == qm2.units)
        self.assertTrue(not(qm1.units == qft.units))

    def test_smart_unit_notequal(self):
        """ test smart unit class __ne__ method"""
        qm1 = Quantity(1, units='m', family_name='depth')
        qm2 = Quantity(2, units='m', family_name='depth')
        qft = Quantity(1, units='feet', family_name='depth')

        self.assertTrue(not(qm1.units != qm2.units))
        self.assertTrue(qm1.units != qft.units)

    def test_get_family_name(self):
        """ test get_family_name with standard and ?/* type matching """

        self.assertEqual(unit_manager.get_family_name('svelo'), 'svelocity')
        self.assertEqual(unit_manager.get_family_name('vpsand'), 'pvelocity')

    def test_unit_system_units_call(self):
        """ test call to a unit_system's 'units' method """

        kgs = unit_manager.lookup_system('KGS')
        # do some funny stuff to get 'almost_equal' testing
        # first test 'value'
        self.assertAlmostEqual(
            kgs.units('rhog').value,
            unit_parser.parse_unit('1000*kg/m**3').value)
        self.assertAlmostEqual(
            kgs.units('pvelocity').value,
            unit_parser.parse_unit('1000*m/s').value)
        # now make sure derivations match
        self.assertEqual(kgs.units('rhog').derivation,
                         unit_parser.parse_unit('1000*kg/m**3').derivation)
        self.assertEqual(
            kgs.units('pvelocity').derivation,
            unit_parser.parse_unit('1000*m/s').derivation)

    def test_ppg(self):
        # PPG is a density measurement. It is not a pressure gradient unit. The
        # pressure gradient can be found by multiplying the density by the
        # acceleration due to gravity.
        self.assertEqual(geo_units.ppg.derivation, density.gcc.derivation)

    #########################################################################
    # Private Methods:
    #########################################################################

    def _compute_force(self, mass, acc, mass_units=kg,
                       acc_units=ms2, **unused_units):
        """
        """
        # algorithm units are
        mass_u = kg
        acc_u = ms2
        # convert into algorithm units
        mass = units.convert(mass, mass_units, mass_u)
        acc = units.convert(acc, acc_units, acc_u)
        # do the math :-)
        return mass * acc


class TestTimeUnits(unittest.TestCase):
    def test_convert(self):
        t1 = units.convert(1, time.year, time.second)
        self.assertAlmostEqual(t1, (365.25 * 24 * 60 * 60), 6)

        t1 = units.convert(1, time.week, time.second)
        self.assertAlmostEqual(t1, (7 * 24 * 60 * 60))

        t1 = units.convert(1, time.day, time.second)
        self.assertAlmostEqual(t1, (24 * 60 * 60))

        t1 = units.convert(1, time.hour, time.second)
        self.assertAlmostEqual(t1, 60 * 60)

        t1 = units.convert(1, time.minute, time.second)
        self.assertAlmostEqual(t1, 60)

    def test_convert_str(self):
        t1 = convert_str(1, "year", "second")
        self.assertAlmostEqual(t1, (365.25 * 24 * 60 * 60), 6)

        t1 = convert_str(1, "week", "s")
        self.assertAlmostEqual(t1, (7 * 24 * 60 * 60))

        t1 = convert_str(1, "day", "sec")
        self.assertAlmostEqual(t1, (24 * 60 * 60))

        t1 = convert_str(1, "hour", "second")
        self.assertAlmostEqual(t1, 60 * 60)

        t1 = convert_str(1, "minute", "second")
        self.assertAlmostEqual(t1, 60)

        t1 = convert_str(1, "minutes", "second")
        self.assertAlmostEqual(t1, 60)


class TestAngleUnits(unittest.TestCase):
    def test_convert(self):
        t1 = units.convert(60, angle.minutes, angle.degree)
        self.assertAlmostEqual(t1, 1)

        t1 = units.convert(3600, angle.seconds, angle.degree)
        self.assertAlmostEqual(t1, 1)

        t1 = units.convert(1, angle.degree, angle.radian)
        self.assertAlmostEqual(t1, numpy.pi / 180.)

    def test_convert_str(self):
        t1 = convert_str(60, "'", "deg")
        self.assertAlmostEqual(t1, 1)

        t1 = convert_str(3600, '"', "deg")
        self.assertAlmostEqual(t1, 1)

        t1 = convert_str(1, 'deg', "rad")
        self.assertAlmostEqual(t1, numpy.pi / 180.)
