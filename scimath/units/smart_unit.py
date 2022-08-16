# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Extends unit capability to include offsets and pretty printing.
"""

#############################################################################
# Imports:
#############################################################################
import warnings
import numpy

# Local imports.
from scimath.units.convert import convert
from scimath.units.SI import dimensionless

from scimath.units.unit import unit


class OffsetUnit(unit):
    """ Special unit to handle temperatures as absolutes--including offsets """

    def __init__(self, factor, derivation, offset=0.0):
        warnings.warn("Using the OffsetUnit class is not recommended as its offset"
                      " attribute is now available on the more general parent "
                      "class: scimath.units.unit.unit.")
        unit.__init__(self, factor, derivation)
        self.offset = offset

    def __eq__(self, other):
        """ return true if self and other are the same """
        return (super(OffsetUnit, self).__eq__(other)
                and hasattr(self, 'offset')
                and hasattr(other, 'offset')
                and (self.offset == other.offset))

    def __ne__(self, other):
        """ return true if self and other are not the same """
        return (super(OffsetUnit, self).__ne__(other)
                or (hasattr(self, 'offset')
                    and hasattr(other, 'offset')
                    and (self.offset != other.offset)))


class SmartUnit(OffsetUnit):
    """ This class inherits from `OffsetUnit`, which extends `units.unit.unit`
    to handle the case of units with an offset, such as temperatures. SmartUnit
    adds the capability to add a pretty label such as 'g/cc' to display instead
    of '1000*kg*m**-3'.
    """

    def __init__(self, label, value, derivation, offset, valid):

        self.label = label
        self.value = value
        self.derivation = derivation
        self.offset = offset
        self.valid = valid

    def __eq__(self, other):
        """ return true if self and other are the same """
        return (super(OffsetUnit, self).__eq__(other)
                and ((hasattr(other, 'offset') and self.offset == other.offset)
                     or self.offset == 0))

    def is_valid(self):
        return self.valid

    def get_label(self):
        return self.label

    def __str__(self):
        """ Returns the pretty units label if it exists.
        """
        if isinstance(self.value, numpy.ndarray):
            st = "<array>"
        elif self.label is not None:
            return self.label
        else:
            st = str(self.value)
        derivation = self._strDerivation()
        if not derivation:
            return st

        return st + "*" + derivation

    def can_convert(self, new_unit):
        """ If `units.convert()` fails to run then the two units
        systems specified are probably not consistent.
        """
        # parse errors generate dimensionless units so if they both end up
        # being dimensionless but invalid convert() will not throw an exception
        if not self.is_valid() or not new_unit.is_valid():
            return False

        try:
            convert(1.0, self, new_unit)
            ok = True
        except Exception as msg:
            ok = False

        return ok


def is_dimensionless(unit):
    """ Determines whether a unit is dimensionless, i.e., has no units.
    """
    if unit.derivation == dimensionless.derivation:
        return True

    return False
