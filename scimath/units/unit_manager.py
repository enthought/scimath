# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Looks after known unit systems and type converters.
"""

#############################################################################
# Imports:
#############################################################################

# Standard library imports.
from fnmatch import fnmatch
import logging

# Enthought library imports.
from traits.api  import HasTraits, HasPrivateTraits, Trait, List, Dict, \
    Instance, Str, Any, Int

# local imports
from scimath.units.unit_db import UnitDB
from scimath.units.unit_system import UnitSystem
from scimath.units.unit_converter import default_unit_converters
from scimath.units.convert import convert as unit_convert
from .unit import unit
from .unit_parser import unit_parser


logger = logging.getLogger(__name__)


class UnitFamily(HasPrivateTraits):
    """ Simple object to store family name, inverse and description """

    family_name = Str
    description = Str
    inverse = Str

    def __init__(self, family_name, description, inverse):

        self.family_name = family_name
        self.description = description
        self.inverse = inverse


class UnitCache(HasTraits):

    max_size = Int(100)
    cache = Dict

    def lookup(self, name):
        """ Tries to find the value for key name in the cache. Throws a
            KeyError if the name is not in the cache. """

        return self.cache[name]

    def add(self, name, value):

        if len(self.cache) < self.max_size:
            self.cache[name] = value
        else:
            # randomly remove an item from the cache to make way for the
            # new one
            self.cache.popitem()
            self.cache[name] = value

    def reset(self):
        self.cache = {}


class UnitManager(HasPrivateTraits):
    """ The unit manager to be used as a singleton in a particular application

    The unit manager looks after all known unit systems, tracks the 'default'
    unit system and manages the unit converters dictionary

    """

    unit_systems = List(Instance(UnitSystem))
    unit_converters = Dict(Str, Any)
    unit_members = Dict(Str, Str)
    preferred_names = Dict(Str, Str)
    default_system = Instance(UnitSystem)
    unit_families = Dict(Str, Instance(UnitFamily))

    _family_cache = Instance(UnitCache)

    def __init__(self):
        """ Creates a new unit manager. """

        self._family_cache = UnitCache(max_size=200)
        self._wildcards = []
        # instantiate default UnitDB object using default text files:
        udb = UnitDB()
        udb.get_family_members_from_file()
        udb.get_unit_families_from_file()

        # Add each unit system from unit_db defaults
        for udb_sys in udb.unit_systems:

            us = UnitSystem(udb_sys)

            # set the system's manager to myself--workaround for former
            # circular dependency
            us.unit_manager = self

            column_name = '%s_%s' % (udb_sys.upper(), 'UNITS')

            for fam in udb.unit_names:
                us.add_family(fam,
                              udb.unit_names[fam][
                                  udb.column_names[column_name]],
                              description=udb.unit_names[fam][
                                  udb.column_names['DESCRIPTION']],
                              inverse=udb.unit_names[fam][udb.column_names['INVERSE']])

            self.add_unit_system(us)

        # Add unit members/preferred names from unit_db defaults
        self.unit_members = udb.member_names
        self.preferred_names = udb.preferred_names

        for name in udb.member_names:
            if name.find('*') != -1:
                self._wildcards.append(name)

        # Load unit converters from default_unit_converters file
        self.unit_converters = default_unit_converters

        self.default_system = self.unit_systems[0]

    ###########################################################################
    # 'UnitManager' interface.
    ###########################################################################

    def add_unit_system(self, unit_system):
        """ Allows addition of new system at run-time.  This is also used by
            at initialization to populate systems known by the unit_manager
            from a unit_db (loaded from a text file) """

        self.unit_systems.append(unit_system)

    def get_default(self):
        """ Returns the default unit system. """

        return self.default_system

    def set_default(self, system):
        """ Sets the default unit system.

        Probably called when the project is loaded.

        """
        if isinstance(system, str):
            self.default_system = self.lookup_system(system.upper())

        elif isinstance(system, UnitSystem):
            self.default_system = system

        else:
            self.default_system = self.unit_systems[0]

        logger.info(
            "Unit manager - default unit system set to: %s" %
            self.default_system)

    def lookup_system(self, name):
        """ Returns the unit system with the specified name or raises
        an exception if no such system exists.
        """

        # FIXME: Consider using a map to store the unit systems?
        for unit_system in self.unit_systems:
            if str(unit_system) == name:
                break

        else:
            msg = "Unknown unit system: %s.  Currently available systems are %s" \
                % (name, [us.name for us in self.unit_systems])
            raise KeyError(msg)

        return unit_system

    def get_unit_system(self, system=None):
        """ Used to simplify the method change_unit_system()
        method that can take a String, an UnitSystem or None.
        """

        try:
            # case #1 - supplied an actual unit system
            if isinstance(system, UnitSystem):
                result = system
            # case #2 - system specified as a string eg 'IMPERIAL'
            elif isinstance(system, str):
                result = self.lookup_system(system.upper())
            # case #3 - no system supplied so use the unit_manager's default
            elif system is None:
                result = self.get_default()
            # who knows what the user passed us?
            else:
                raise Exception

        except Exception as msg:
            logger.exception("Unrecognized unit system %s" % system)
            result = self.get_default()

        return result

    def add_system(self, system):
        """ Adds unit system(s) to the unit_manager's list of systems
        """
        self.unit_systems.append(system)

    def add_member(self, member_name, family):
        """ Adds a member to the unit_members dict used to lookup unit aliases

            Parameters
            ----------
            member_name:
                the alias

            family:
                the name of the unit_family to which the alias maps
        """

        self.unit_members[member_name] = family
        if member_name.find('*') != -1:
            self._wildcards.append(member_name)
        # clear out the cache
        self._family_cache.reset()

    def add_family(self, family_name, description, inverse):
        """ Maintains dict of families w/ description & inverse values """

        self.unit_families[family_name] = UnitFamily(family_name,
                                                     description, inverse)

    def get_family_name(self, name):
        """ Returns family name given a member name """

        # keep from going through the fnmatch case on an empty name
        if name == '' or name is None:
            return 'unknown'

        try:
            # if this name appears in our lookup cache then just return the
            # result
            return self._family_cache.lookup(name)
        except KeyError:
            pass

        # Strip off common prefix that will cause matching to fail.
        if name.startswith('copy_of'):
            name = name[8:]

        orig_name = name

        # Successively remove _x at end of name and check for match
        # If name has no '_', this yields name = ''
        while name != '' and name not in self.unit_members:
            name = '_'.join(name.split('_')[:-1])

        if name == '':
            # No match yet...
            # Try to more aggressively match by checking for * and ? matches
            for itm in self._wildcards:
                if fnmatch(orig_name, itm):
                    name = itm
                    break

        # Still no match
        if name == '':
            family_name = 'unknown'
        else:
            family_name = self.unit_members[name]

        self._family_cache.add(orig_name, family_name)

        return family_name

    def get_valid_units(self, family_name):
        """ Returns a list of units that are compatible with
            a family given a family name (or alias)"""

        valid_units = []
        # get family name, just in case an alias was provided
        family_name = self.get_family_name(family_name)

        for usys in self.unit_systems:
            unit = usys.units(family_name)
            if unit not in valid_units:
                valid_units.append(unit)

        valid_units.sort(key=lambda x: x.label)

        return valid_units

    def get_valid_unit_strings(self, family_name):
        """ Returns a list of units that are compatible with
            a family given a family name (or alias)"""

        valid_units = sorted(
            [x.label for x in self.get_valid_units(family_name)])

        return valid_units

    def get_inverse_family_name(self, family_name):
        """ Returns the inverse family name of the given family name
            (or member name) """

        try:
            family_name = self.get_family_name(family_name)
            inverse_family = self.unit_families[family_name].inverse
            return inverse_family

        except KeyError:
            logger.exception("Unrecognized family: %s" % family_name)
            raise

    def get_inverse_name(self, family_name):
        """ Returns the 'preferred' name of the inverse of the given
            family name (or member name) """

        family_name = self.get_family_name(family_name)
        inverse_family = self.get_inverse_family_name(family_name)

        return self.preferred_names[inverse_family]

    def get_family_name_for_value(self, unit_value):
        """ Walks the unit_db looking for a unit with a matching value.
            This is potentially expensive, so only do it if you must.

        """
        for family_name in self.unit_families:
            if unit_value in self.get_valid_units(family_name):
                return family_name

        return None

    def is_compatible(self, units, family_name):
        """ Returns True if the family_name and units are compatible.
        Just because two units have the same derivation, does not mean they
        are compatible, it just means that value conversion is simple.
        """
        if units is None:
            units_label = None

        elif isinstance(units, unit):
            units_label = units.label

        elif isinstance(units, str):
            units_label = units
            units = unit_parser.parse_unit(units)

        # Unknown logs are not unit converted
        # so any unit name is ok
        if family_name == 'unknown':
            return True

        if units_label in self.get_valid_unit_strings(family_name):
            return True

        if family_name != 'none' and units_label in ['none', 'unknown']:
            return False

        try:
            default_units = self.default_units_for(family_name)
            unit_convert(1.0, units, default_units)
            return True

        except:
            pass

        return False

    def are_compatible_families(self, family1, family2):
        """ Returns True if family2 is compatible with family1.
        Equal families are compatible.  All families are compatible with None.
        That is when family1 is 'None' any value for family2 is considered
        compatible.
        """
        return family1.lower() == 'none' or family1 == family2

    def default_units_for(self, family_name):
        """ Returns the default unit system units for the specified family. """

        unit_system = self.get_default()

        return unit_system.units(family_name)

    def default_units_for_name(self, name):
        """ Return the units in the default unit system for the name.
        name must be a member of a family.
        """
        family_name = self.get_family_name(name)
        units = self.default_units_for(family_name)
        return units

    def change_unit_system(self, obj, new_unit_system=None):
        """ Changes unit system for supported object types.

        Supported types are types with a registered unit conversion function.
        This unit conversion function will be invoked to return a new object
        whose data is equal to the data of obj converted to new_unit_system.
        If new_unit_system is unspecified, the target unit system is the
        system default unit system.

        If the units cannot be converted (i.e., a Quantity instance has no
        family_name), an exception is logged and raised.
        """

        new_unit_system = self.get_unit_system(new_unit_system)

        try:
            conv_func = self.get_unit_converter(obj)
            result = conv_func(obj, new_unit_system)

            # If we converted a quantity, attach the original quantity to the
            # _converted_from trait so we can propagate changes back.
            from scimath.units.quantity import Quantity
            if isinstance(result, Quantity):
                # FIXME : Is the previous check necessary? Do we ever convert
                # non-quantities?
                result._converted_from = obj

            return result

        except:
            logger.warning("Could not convert object: %s to system: %s" %
                           (obj, new_unit_system))
            raise

    def convert(self, obj, new_unit_system=None):
        """ Convert obj to specified new_unit_system
            new_unit_system may be a unit_system or a string or
            None (default) if you wish to use the default system
            """
        new_unit_system = self.get_unit_system(new_unit_system)

        try:
            conv_func = self.get_unit_converter(obj)
            return conv_func(obj, new_unit_system)

        except Exception as ex:
            logger.exception(ex)
            logger.warning("Could not convert object: %s to system: %s" %
                           (obj, new_unit_system))
            return obj

    def get_unit_converter(self, obj):
        """ Convenience function to lookup converter """

        return self.unit_converters[str(obj.__class__)]

    ##########################################################################
    # Private Interface
    ##########################################################################

    # TODO: this method does not seem to ever be called--consider deleting.
    def _convert(self, value, from_units, to_units):

        if isinstance(value, str):
            converted_data = value.data
        elif isinstance( value, numpy.ndarray) and \
                value.dtype.char == 'S':
            converted_data = value
        else:
            converted_data = unit_convert(value, from_units, to_units)

        return converted_data

# The as-yet unenforced singleton instance

unit_manager = UnitManager()


class IncompatibleUnitFamilies(Exception):

    def __init__(self, fromFamily, toFamily):
        self._toFamily = toFamily
        self._fromFamily = fromFamily

    def __str__(self):
        str = "Cannot convert across unit families: '%s' and '%s'" % \
              (self._toFamily, self._fromFamily)
        return str
