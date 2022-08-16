# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines an AQuantity trait with supporting editors for use with
objects containing Quantity values.
"""
#-------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------

from traits.api \
    import Trait, TraitFactory, TraitHandler

from .quantity \
    import Quantity

#-------------------------------------------------------------------------
#  'AQuantity' trait factory:
#-------------------------------------------------------------------------


def AQuantity(value=1.0, units= 'm', family = '', **metadata):
    quantity = Quantity(value, units, family_name=family)
    return Trait(quantity, QuantityTraitHandler(quantity), **metadata)

AQuantity = TraitFactory(AQuantity)

#-------------------------------------------------------------------------
#  'QuantityTraitHandler' class:
#-------------------------------------------------------------------------


class QuantityTraitHandler (TraitHandler):

    #-------------------------------------------------------------------------
    #  Initializes the object:
    #-------------------------------------------------------------------------

    def __init__(self, quantity):
        self.quantity = quantity

    def validate(self, object, name, value):
        try:
            if self.quantity.units.can_convert(value.units):
                return value
        except:
            pass
        self.error(object, name, value)

    def post_setattr(self, object, name, value):
        q = self.quantity
        object.__dict__[ name + '_' ] = \
            Quantity(value, q.units, q.name, family_name=q.family_name)

    def info(self):
        return "a quantity which is convertible to '%s'" % self.quantity.units
