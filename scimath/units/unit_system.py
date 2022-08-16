# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines the UnitSystem class
"""

#############################################################################
# Imports:
#############################################################################
# Standard library imports.
import logging

# Enthought library imports.
from traits.api import HasTraits, Instance, Str, Dict, Any

# Local Imports:
from scimath.units.convert import convert as units_convert
from scimath.units.unit_parser import unit_parser


logger = logging.getLogger(__name__)


class UnitSystem(HasTraits):
    """
    A UnitSystem represents a set of 'units' designations for a list of
    families.  This is initially populated from the columns in the
    scimath/units/data/unit_families.txt file (by the unit_manager).

    The common unit systems are likely named 'KGS', 'IMPERIAL' etc.
    """

    # Unit System Traits
    unit_manager = Any
    # commented for testing...
    #unit_manager = Instance('scimath.units.unit_manager.UnitManager', copy='shallow')
    name = Str
    families = Dict

    def __init__(self, name, families={}):

        # the name of the unit system eg 'KGS' or 'IMPERIAL'
        self.name = name.upper()

        # TODO: consider not accepting a families dict as an argument at all
        # and just use the add_family method.
        if families:
            for fam in families:
                # not sure how to accept args here--right now families is a
                # dictionary of keys and lists, where the list contains
                # [unit, description, inverse]
                self.add_family(
                    fam,
                    families[fam][0],
                    families[1],
                    families[2])

    def units(self, name):
        """ Method to return a unit for a given family or member name """

        # TODO: This seems like a very slow way to do this
        result = self.families.get(name, self.families.get(
            self.unit_manager.unit_members.get(
                self.unit_manager.get_family_name(name))))

        if not result:
            logger.exception('Could not find %s in this unit_system' % name)
        return result

    def add_family(self, family_name, fam_unit,
                   description=None, inverse=None):
        """ Add to families dictionary

            parameters
            ----------
            family_name:
                name of family--also sets preferred_name

            system_units:
                either an scimath.units.unit type or a string that may be
                coerced into a unit type.

        """

        # convert string to unit
        if isinstance(fam_unit, type('')):
            fam_unit = unit_parser.parse_unit(fam_unit)

        self.families[family_name] = fam_unit

        # if this system has a unit manager and the description or inverse
        # arguments are provided, populate this system's um.unit_families
        # as well.
        if self.unit_manager and (description or inverse):
            self.unit_manager.add_family(family_name, description, inverse)

    def get_manager_families(self):
        """ Convenience method to get the dict of families from
            this UnitSystem's unit_manager """

        return self.unit_manager.unit_families

    def __str__(self):
        return self.name

    #########################################################################
    # UnitSystem Interface
    #########################################################################

    def get_family_name(self, quant_name):
        """ Returns the family name for a given alias (member)
        """
        try:
            fam_name = self.unit_manager.unit_members[quant_name]
        except KeyError:
            logger.exception(
                'Could not find a family name for %s' %
                quant_name)
            fam_name = None
        return fam_name

    def get_inverse_log_name(self, quant_name):
        """ Returns the default name of the inverted log
        """
        # fixme - why are these here?
        try:
            inv_name = self.unit_manager.unit_families[
                self.get_family_name(quant_name)].inverse
        except KeyError:
            logger.exception(
                'Could not find an inverse log name for %s' %
                quant_name)
            inv_name = None
        return inv_name


# Single copy of the standard unit system used by algorithms.

#kgs = UnitSystem('KGS')
