# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
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

        self.failUnlessEqual(mq.name, 'vp')
        self.failUnlessEqual(mq.units.label, 'km/s')
        self.failUnlessEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_compatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.name = 'vs'
        mq.family_name = 'svelocity'
        self.failUnlessEqual(mq.name, 'vs')
        self.failUnlessEqual(mq.units.label, 'km/s')
        self.failUnlessEqual(mq.family_name, 'svelocity')
        return

    def test_metaquantity_compatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.units = 'ft/s'
        self.failUnlessEqual(mq.name, 'vp')
        self.failUnlessEqual(mq.units.label, 'ft/s')
        self.failUnlessEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_incompatible_units_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        self.failUnlessRaises(TraitError, setattr, mq, 'units', 'hours')

        self.failUnlessEqual(mq.name, 'vp')
        self.failUnlessEqual(mq.units.label, 'km/s')
        self.failUnlessEqual(mq.family_name, 'pvelocity')
        return

    def test_metaquantity_incompatible_family_change(self):
        mq = MetaQuantity(name='vp', units='km/s', family_name='pvelocity')

        mq.family_name = 'time'

        self.failUnlessEqual(mq.name, 'vp')
        self.failUnlessEqual(mq.units.label, 'msec')
        self.failUnlessEqual(mq.family_name, 'time')
        return

    def ui_simple(self):
        mq = MetaQuantity()
        mq.configure_traits(kind='modal')
        print('\n')
        mq.print_traits()
        return
