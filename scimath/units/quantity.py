# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines Quantity class.
"""

# Standard library imports.
import logging
import numpy

# Enthought library imports.
from traits.api import Any, HasPrivateTraits, Instance, Str

# Local imports
from scimath.units.convert import convert as units_convert
from scimath.units.SI import dimensionless
from scimath.units.unit import unit
from scimath.units.smart_unit import SmartUnit
from scimath.units.unit_parser import unit_parser
from scimath.units.unit_manager import unit_manager
from scimath.units.family_name_trait import FamilyNameTrait


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class Quantity(HasPrivateTraits):
    """ A Quantity is a data item (usually scalar or array) with
        associated units and name.

        Attributes
        ----------
        data
            scalar, `array`, or `Quantity`: A scalar value array of
            values.
        units: `unit`
            A units object that defines the type of
            units for values in the data attribute.
        name: `string`
            Default is the empty string.  Name of the Quantity.
            This is useful as a label for plots, etc.
        family_name: `string`
            Used for unit_system conversion and keyed by styles

        Description
        -----------
        A Quantity object is used to associate units and perhaps a name with
        a scalar value or array of values.  It is little more than a structure
        to group this information together.

        Examples
        --------

        >>> # scalar example
        >>> from units.SI import meter, second
        >>> Quantity(2.2, meter/second)
        Quantity(2.2, 1.0*m*s**-1)

        >>> # an array example
        >>> from numpy import arange
        >>> data = arange(3.)
        >>> Quantity(data, meter, 'depth')
        Quantity(depth, [ 0.  1.  2.], 1.0*m)
    """

    #### Traits ###############################################################

    # A scalar value array of values.
    data = Any

    # A units object that defines the type of units for values in data.
    units = Any

    # TODO: fix bug here where a unit is not recognized as a unit.
    #units = Trait(dimensionless, unit)

    # Family to use for unit system conversion.
    family_name = FamilyNameTrait

    # The displayable name of the quantity (e.g., used as label on plots).
    name = Str

    # The source quantity if this quantity is converted from another quantity.
    _converted_from = Instance('Quantity')

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, data, units=None, name='', **traits):
        """ Constructor. """

        # Base class constructors.
        super(Quantity, self).__init__(**traits)

        # Flag used to save a compare if units/family_name compatibility has
        # already been validated.
        compatibility_checked = None

        self.name = name

        # Determine what units to use and if they are family compatible.
        if units is None:
            units = unit_manager.default_units_for(self.family_name)

        # Allow for parsing a unit string as the units argument
        else:
            if isinstance(units, str):
                units = unit_parser.parse_unit(units, suppress_warnings=False)

        if 'family_name' not in traits:
            # If the family name wasn't passed in, we try to guess it.
            # TODO: Should lower() be called here--one can do an
            # 'obj.family_name='xxx'" that would not call a 'lower' method.

            try:
                um = unit_manager
                if self.family_name is None:
                    family_name = ''
                else:
                    family_name = self.family_name.lower()
                self.family_name = \
                    um.get_family_name(family_name) or \
                    um.get_family_name(name.lower())

                # If units were passed in, but don't match the guessed family_name,
                # punt.
                if not unit_manager.is_compatible(units, self.family_name):
                    self.family_name = "unknown"
                    compatibility_checked = True

            except KeyError:
                logger.warn("Could not find family name: %s" %
                            self.family_name or name)
        else:
            # fixme: This is subverting the FamilyNameTrait behavior,
            #        but it gets around proava ticket:1715-comment14,item 2.
            self.family_name = traits['family_name']

        # If we haven't checked compatibility before, and units
        if (compatibility_checked != True and
                not unit_manager.is_compatible(units, self.family_name)):
            raise ValueError("units (%s) not compatible with family_name (%s)"
                             % (units.label, self.family_name))

        self.units = units

        # The following timing data is from using the code below the
        #     timings that sets values for 'data' and 'units' using the
        #     'slow' method.

        if isinstance(data, Quantity):
            self.data = self._convert(data, units)
        else:
            self.data = data

        # The 'fast' method of just stuffing the __dict__ values yields a
        #     performance improvement of 2x-- 0.0016 sec vs. 0.0035 sec per
        #     unit change (which creates a new Quantity object).

        #self.__dict__['data'] = self._convert(data, units)
        #self.__dict__['units'] = units

    def __repr__(self):
        """ Return the string representation of this quantity. """

        if isinstance(self.data, numpy.ndarray):
            data_repr = '<array>'

        else:
            data_repr = self.data

        return '%s(name=%s, data=%s, units=%s, family_name=%s)' % \
            (self.__class__.__name__,
             self.name, data_repr, self.units, self.family_name)

    ########################################################################
    # 'HasTraits' interface.
    ########################################################################

    def trait_view(self, name=None, view_element=None):
        """ Return view object for self. """
        if (name or view_element) is not None:
            return super(Quantity, self).trait_view(name=name,
                                                    view_element=view_element)

        from scimath.units.ui.quantity_view import QuantityView
        view = QuantityView()
        view.title = self.name

        return view

    def edit_traits(self, view=None, context=None, naming_context=None,
                    **args):
        """ Displays a user interface window for editing trait attribute values.

        naming_context - context in which the quantity is bound.  Editor will
            use this to ensure name uniqueness.
        """
        if context is None:
            context = self.trait_context()

        context['naming_context'] = naming_context

        return super(Quantity, self).edit_traits(view=view, context=context,
                                                 **args)

    ########################################################################
    # 'HasTraitsPlus' interface.
    ########################################################################

    def clone(self):
        """ Returns a clone of the object. """

        # delayed import until we know we need this sooner.
        if isinstance(self.data, numpy.ndarray):
            data = self.data.copy()

        else:
            data = self.data

        clone = self.__class__(
            data,
            name=self.name,
            units=self.units,
        )

        # Note:  This is done outside of the context of the constructor in case
        # we are cloning a quantity with mis-matched units and family name
        clone.family_name = self.family_name

        return clone

    ########################################################################
    # Public 'Quantity' interface.
    ########################################################################

    def change_unit_system(self, new_unit_system=None, **kw):
        """ Convenience method for changing a quantity's units according to
            a given unit system.  This just calls the unit_manager's method
            to do this.
            Keyword args are passed on to the converter.
            """

        # FIXME: TODO: Keyword args should be passed on to the converter.
        return unit_manager.change_unit_system(self, new_unit_system)

    def get_unit_converter(self):
        """ Convenience function to lookup converter """

        return unit_manager.get_unit_converter(self)

    def invert(self, unit_system=None):
        """ Inverts quantity to units, family and name listed by unit manager
            as the quantity inverse. """

        try:
            inverse_family = unit_manager.get_inverse_family_name(
                self.family_name)
            inverse_name = unit_manager.get_inverse_name(self.family_name)

            new_quantity = self.clone()
            new_quantity.data = 1.0 / self.data
            new_quantity.units = 1.0 / self.units
            new_quantity.family_name = inverse_family
            new_quantity.name = inverse_name
            # Call to set the inverted quantity to the units of the current
            #      unit system.
            result = new_quantity.change_unit_system()
            return result

        except KeyError:
            logger.warn("Could not find inverse of family %s" %
                        self.family_name)

    def propagate_data_changes(self):
        """ Propagate data changes up the conversion stack.

        Unit conversions create a stack of quantities in different unit
        systems, represented by the _converted_from trait.  This method
        propagates changes to the data trait back up that conversion stack
        by converting the units from the current quantity to the units of
        the predecessor quantity and replacing the data trait.  Propagation
        continues until an original quantity is encountered.

        In theory, this method could raise an exception if the units cannot
        be converted back.  This would imply the unit_family has been changed
        back to None.
        """

        predecessor = self._converted_from

        # If predecessor is none, this is an original quantity.
        if predecessor is None:
            return

        # Replace the predecessor's data with converted data.
        new_quantity = self.change_unit_system(predecessor.units)
        predecessor.data = new_quantity.data

        # Recursively continue propagating.
        predecessor.propagate_data_changes()

    def get_original(self):
        """ Returns the original quantity in the conversion stack. """

        predecessor = self._converted_from

        # If predecessor is None, this is an original quantity.
        if predecessor is None:
            result = self

        # Otherwise, walk the stack.
        else:
            result = predecessor.get_original()

        return result

    ########################################################################
    # Private interface.
    ########################################################################

    def _convert(self, data, units):
        """ Handles the conversion to the desired units.

        If the incoming object is NOT a Quantity object, just returns the data.
        """

        if isinstance(data, Quantity):
            # if data is a string or an array of strings, ignore the conversion
            # because convert will fail for string data
            if isinstance(data.data, str):
                converted_data = data.data
            elif isinstance(data.data, numpy.ndarray) \
                    and data.data.dtype.char == 'S':
                converted_data = data.data
            else:
                converted_data = units_convert(data.data, data.units, units)
        else:
            converted_data = data

        return converted_data
