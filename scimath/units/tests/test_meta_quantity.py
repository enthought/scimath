# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

from traits.api import TraitError

from scimath.units.api import MetaQuantity


class TraitsTestCase(TestCase):

    def test_metaquantity(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'pvelocity')

    def test_metaquantity_compatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.name = 'vs'
        mq.family_name = 'svelocity'
        self.assertEqual(mq.name, 'vs')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'svelocity')

    def test_metaquantity_compatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.units = 'ft/s'
        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'ft/s')
        self.assertEqual(mq.family_name, 'pvelocity')

    def test_metaquantity_incompatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        self.assertRaises(TraitError, setattr, mq, 'units', 'hours')
        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'pvelocity')

    def test_metaquantity_incompatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.family_name = 'time'

        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'msec')
        self.assertEqual(mq.family_name, 'time')

    def ui_simple(self):
        mq = MetaQuantity()
        mq.configure_traits(kind='modal')
        print('\n')
        mq.print_traits()
