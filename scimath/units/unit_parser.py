#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2003  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Standard library imports.
import ast
import logging
import re

# Local imports.
from scimath.units.unit import unit
from scimath.units.SI import dimensionless
from scimath.units.smart_unit import SmartUnit


logger = logging.getLogger(__name__)


#factory method
def parser():
    return Parser()

# implementation of the Parser singleton
class Singleton:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state


class Parser(Singleton):

    def extend(self, *modules):
        for module in modules:
            self.context.update(module.__dict__)
        self._cleanContext(context)
        self._cacheExactLabels()

    def parse(self, string):
        # FIXME: we should compile this to an AST, whitelist the
        # arithmetic operations, numbers, and the names in our context
        # before evaluating.
        self.context['__builtins__'] = None
        try:
            value = eval(string, self.context)
        except Exception:
            if string in self.exact_labels:
                return self.exact_labels[string]
            else:
                raise
        finally:
            self.context.pop('__builtins__', None)
        return value

    def init(self, *args, **kwds):
        self.context = self._initializeContext()
        self._cacheExactLabels()

    def _initializeContext(self):
        context = {}
        modules = self._loadModules()
        for module in  modules:
            context.update(module.__dict__)
        self._cleanContext(context)
        # Add the SI names used in the derivations and labels but not
        # already in the context.
        context['A'] = context['amp']
        context['cd'] = context['candela']
        context['S'] = context['siemens']
        return context

    def _cleanContext(self, context):
        """ Remove any non-unit from the context.

        Numbers can remain.
        """
        for name in list(context):
            if not isinstance(context[name], (float, int, unit)):
                del context[name]

    def _cacheExactLabels(self):
        self.exact_labels = {}
        for name, value in self.context.items():
            if isinstance(value, unit) and value.label is not None:
                self.exact_labels[value.label] = value

    def _loadModules(self):

        import SI
        import acceleration
        import angle
        import area
        import density
        import dimensionless
        import electromagnetism
        import energy
        import force
        import frequency
        import length
        import mass
        import power
        import pressure
        import speed
        import substance
        import temperature
        import time
        import volume
        import geo_units

        modules = [
            SI, acceleration, angle, area, density, dimensionless,
            electromagnetism, energy, force, frequency, length, mass, power,
            pressure, speed, substance, temperature, time, volume, geo_units
        ]

        return modules


class UnitParser:

    def __init__(self):

        # Init the main unit parser
        self.parser = parser()
        self.parser.init()

        # TODO: factor out--adjust to scimath.units
        # In fact, the unit manager should extend this when a new 'system' or
        # unit set is set up.

        # We have defined many units commonly used by geophysicists .....
        # import cp.units.geo_units
        #self.parser.extend(cp.units.geo_units)

        # This is used to clean up labels like ohm.m in remove_dots()
        self.regex = re.compile(r'([A-Za-z])\.([A-Za-z])')

        return

    def parse_unit(self, label, suppress_warnings=True, suppress_unknown=True):
        """ Parses a string description of a unit e.g., 'g/cc'.
        if suppress_unknown is True and the label cannot be parsed, the returned
        unit is dimensionless otherwise UnableToParseUnits is raised.
        """

        # someone (or some s/w) writes out units like ohm.m
        label = self.remove_dots(label)

        # retain the user's original description of the unit
        pretty_label = label

        valid = True
        offset_value = 0.0

        # Handle offsets.
        plusses = label.count('+')
        if plusses > 1:
            self._error(label, suppress_warnings, suppress_unknown)
            valid = False
        elif plusses == 1:
            label, offset_label = label.split('+')
            label = label.strip()
            offset_label = offset_label.strip()
            try:
                offset_value = ast.literal_eval(offset_label)
            except Exception:
                self._error(label, suppress_warnings, suppress_unknown)
                valid = False
            else:
                if not isinstance(offset_value, (int, float)):
                    self._error(label, suppress_warnings, suppress_unknown)
                    valid = False
                else:
                    has_offset = True

        # make sure we can parse the label ....
        if label == "%":
            label = "percentage"
        if label.lower() == "v/v decimal" or label == "v/v_decimal":
            label = "v/v"
        if label.lower() == "in":
            label = "inch"

        if (label == None or
                label == '' or
                label == 'None' or
                label.lower() == 'unitless' or
                label.lower() == 'unknown'):
            label = "dimensionless"
            pretty_label = "none"

        try:
            _unit = self.parser.parse(label)
        except:
            try:
                _unit = self.parser.parse(label.lower())
                pretty_label = label.lower()
            except:
                self._error(label, suppress_warnings, suppress_unknown)
                valid = False

        if not valid:
            _unit = dimensionless

        if isinstance(_unit, unit):

            if hasattr(_unit, "offset"):
                offset = _unit.offset
            else:
                offset = 0.0

            offset += offset_value

            _unit = SmartUnit(pretty_label, _unit.value, _unit.derivation,
                              offset, valid)
        else:
            # some dimensionless units such as liters/liters still need to have
            # pretty labels etc.
            _unit = SmartUnit(pretty_label, _unit, dimensionless.derivation,
                              offset_value, valid)

        return _unit


    def remove_dots(self, label):
        """ Some LAS files contain units written like 'ohm.m', which this class
        cannot parse, so this function changes them from 'ohm.m' to 'ohm*m'.
        """

        return self.regex.sub(r"\g<1>*\g<2>", label)

    def standardize(self, label):
        """ returns a standard parseable string from a given label
            i.e. 'G/CC' -> 'g/cc' Throws an exception if it can't parse it."""

        try:
            _unit = self.parser.parse(label)
        except:
            try:
                _unit = self.parser.parse(label.lower())
                label = label.lower()
            except:
                raise UnableToParseUnits(label)

        return label

    def _error(self, label, suppress_warnings, suppress_unknown):
        """ Indicate that there was an error in parsing the label.

        Parameters
        ----------
        label : str
            The problematic label.
        suppress_warnings : bool
            Do not log warnings if True.
        suppress_unknown : bool
            Raise an exception if True.

        Returns
        -------
        u : unit
            The dummy unit to use in place of the parsed unit.

        Raises
        ------
        UnableToParseUnits :
            Raised if `suppress_unknown` is True.
        """
        if not suppress_warnings:
            logger.debug( 'Could not parse unit: %r', label)
        if not suppress_unknown:
            raise UnableToParseUnits(label)

#-------------------------------------------------------------------------------
#  Singleton for unit parsing ....
#-------------------------------------------------------------------------------
unit_parser = UnitParser()



class UnableToParseUnits(Exception):

    def __init__(self, label):
        self.label = label
        return

    def __str__(self):
        str = "Label '%s' is not a parseable unit string." % \
              (self.label)
        return str

#### EOF #######################################################################
