# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines a unit manager that looks after known unit systems and type
converters.
"""

#############################################################################
# Imports:
#############################################################################

# Enthought library imports
from traits.api import HasPrivateTraits, Dict

# local imports
from scimath.units.unit_db import UnitDB


class StyleManager(HasPrivateTraits):
    """ Class used to define a singleton style_manager for use by an
        application to store and manage styles associated with any identifiers.
        In the initial case, it maps family names (units use these) to
        style attributes. """
    # styles is a Dictionary with family name as the key and a dictionary of
    #        `style types` as the value.  The dictionary of style types is the
    #        style type name as the key (i.e. 'color' or 'line') and a setting
    #        as the value--e.g.
    #        {'pvelocity':{'color': 'red, 'line': 'solid', ...}, ...}
    styles = Dict  # fixme: This was 'styles=Dict(Dict)' huh?
    # ranges is a Dictionary with family name as the key and a dictionary of
    #        range settings as the value.  The dictionary of range settings
    #        is the unit_system as the key and a tuple of (left, right) values
    #        as the range values.
    ranges = Dict  # fixme: This was 'ranges=Dict(Dict)' huh?

    def __init__(self):

        udb = UnitDB()

        udb.get_family_format_from_file()
        self.styles = udb.unit_formats

        udb.get_family_ranges_from_file()
        self.ranges = udb.unit_ranges

    ###########################################################################
    # 'StyleManager' interface.
    ###########################################################################

    def get_info(self, obj, info, family_name=None):
        """ Lookup style attribute given a family name and the string
            identifier of the style (i.e. family_name="pvelocity", info="color")
            """

        # for now, assume we can get the family_name from the obj, if needed
        if family_name is None:
            family_name = obj.family_name

        return self.styles[family_name][info]

    def get_range(self, obj=None, family_name=None, unit_system=None):
        """ Returns (left, right) tuple signifying format range for plotting
            typically. """

        from scimath.units.unit_manager import unit_manager

        # for now, assume we can get the family_name from the obj, if needed
        if family_name is None:
            family_name = obj.family_name

        # If unit_system is None, sets to default system, or looks up string
        unit_system = unit_manager.get_unit_system(unit_system)

        return self.ranges[family_name][unit_system.name.lower()]


# The as-yet unenforced singleton instance
style_manager = StyleManager()
