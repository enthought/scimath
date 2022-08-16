# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The specification for Quantity objects. """

from traits.api import HasStrictTraits, Str

from .unit_traits import UnitsTrait
from .family_name_trait import FamilyNameTrait

from .unit_manager import unit_manager


class MetaQuantity(HasStrictTraits):
    """ The specification for Quantity objects. """

    # The displayable name of the quantity (e.g., used as label on plots).
    name = Str

    # Family to use for unit system conversion.
    family_name = FamilyNameTrait('length', is_strict=True, allow_none=False,
                                  units_trait='units')

    # A units object that defines the type of units for values in data.
    units = UnitsTrait('m', is_strict=True, allow_none=False,
                       family_trait='family_name')

    def __init__(self, **traits):
        """ Create a new MetaQuantity. """

        if 'units' in traits and 'family_name' in traits:
            # must be set in the correct order.
            units = traits.pop('units')
            family_name = traits.pop('family_name')

        else:
            units = family_name = None

        super(MetaQuantity, self).__init__(**traits)

        if units is not None:
            self.family_name = family_name
            self.units = units

    ###########################################################################
    # HasTraits interface
    ###########################################################################

    def trait_view(self, name=None, view_element=None):
        """ Returns a View """
        if (name or view_element) is not None:
            return super(MetaQuantity, self).trait_view(name=name,
                                                        view_element=view_element)

        from scimath.units.ui.meta_quantity_view import MetaQuantityView
        return MetaQuantityView()

    ###########################################################################
    # private interface
    ###########################################################################

    def _name_changed(self, old, new):
        """ Name has been changed, reset family_name and units in line with
        the defaults for that name.
        """
        self.family_name = unit_manager.get_family_name(self.name)
