#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Greg Rogers
#
#-----------------------------------------------------------------------------

from unittest import TestCase

from traits.api import TraitError

from scimath.units.api import MetaQuantity


class TraitsTestCase(TestCase):

    def test_metaquantity(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_compatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.name = 'vs'
        mq.family_name = 'svelocity'
        self.assertEqual(mq.name, 'vs')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'svelocity')
        return

    def test_metaquantity_compatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.units = 'ft/s'
        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'ft/s')
        self.assertEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_incompatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        self.failUnlessRaises(TraitError, setattr, mq, 'units', 'hours')

        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'km/s')
        self.assertEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_incompatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.family_name = 'time'

        self.assertEqual(mq.name, 'vp')
        self.assertEqual(mq.units.label, 'msec')
        self.assertEqual(mq.family_name, 'time')
        return

    def ui_simple(self):
        mq = MetaQuantity()
        mq.configure_traits(kind='modal')
        print('\n')
        mq.print_traits()
        return
