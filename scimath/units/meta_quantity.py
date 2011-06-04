#-----------------------------------------------------------------------------
#
#  Copyright (c) 2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Greg Rogers
#
#-----------------------------------------------------------------------------

""" The specification for Quantity objects. """

from traits.api import HasStrictTraits, Str

from unit_traits import UnitsTrait
from family_name_trait import FamilyNameTrait

from unit_manager import unit_manager

class MetaQuantity(HasStrictTraits):
    """ The specification for Quantity objects. """

    # The displayable name of the quantity (e.g., used as label on plots).
    name = Str

    # Family to use for unit system conversion.
    family_name = FamilyNameTrait( 'length', is_strict=True, allow_none=False,
                                   units_trait='units')

    # A units object that defines the type of units for values in data.
    units = UnitsTrait('m', is_strict=True, allow_none=False,
                       family_trait='family_name')

    def __init__(self, **traits):
        """ Create a new MetaQuantity. """

        if traits.has_key('units') and traits.has_key('family_name'):
            # must be set in the correct order.
            units = traits.pop('units')
            family_name = traits.pop('family_name')

        else:
            units = family_name = None

        super(MetaQuantity,self).__init__(**traits)

        if units is not None:
            self.family_name = family_name
            self.units = units

        return

    ###########################################################################
    # HasTraits interface
    ###########################################################################

    def trait_view(self, name=None, view_element=None):
        """ Returns a View """
        if (name or view_element) != None:
            return super(MetaQuantity, self).trait_view( name=name,
                                                view_element=view_element )

        from scimath.units.ui.meta_quantity_view import MetaQuantityView
        return MetaQuantityView()

    ###########################################################################
    # private interface
    ###########################################################################

    def _name_changed(self, old, new):
        """ Name has been changed, reset family_name and units in line with
        the defaults for that name.
        """
        self.family_name = unit_manager.get_family_name( self.name )
        return



### EOF

