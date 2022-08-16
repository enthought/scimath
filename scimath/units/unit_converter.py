# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines dictionary of unit conversion methods by object type.
"""

#############################################################################
# Imports:
#############################################################################

# Standard library imports.
import logging
import numpy

# Enthought library imports.
from scimath.units import convert as units_convert


logger = logging.getLogger(__name__)


def typecode(x):
    try:
        return x.dtype.char
    except AttributeError:
        return x.typecode()


def convert_unit_array(unit_array, unit_system=None, to_unit=None,
                       family_name=None):
    """ Function to convert the units of a unit_array

        Parameters:
        -----------
        unit_array
            Unit_array to be converted
        unit_system
            the unit system of the current unit_array units, defaults to the
            unit_managers default system (current unit_system):
        to_units
            new_units to convert to
        family_name
            provided in cases where the family_name attribute is not present
            in the provided unit_array object

    """
    from scimath.units.unit_array import UnitArray

    if family_name is None and unit_array.units is not None:
        family_name = _get_family_name_for_array(unit_array.units)

    if unit_array.units is None:
        family_name = None

    if to_unit is None:
        unit_system = _get_unit_system()
        try:
            to_unit = unit_system.units(family_name)
        except KeyError:
            logger.exception("Could not convert UnitArray: %s to system: %s" %
                             (unit_array, unit_system))
            return unit_array.copy()

    if unit_array.units == to_unit:
        new_array = UnitArray(unit_array, units=unit_array.units)
    else:
        data = units_convert(unit_array.view(numpy.ndarray),
                             unit_array.units, to_unit)
        new_array = UnitArray(data, units=to_unit)

    return new_array


def convert_quantity(q, unit_system=None, to_unit=None, family_name=None):
    if family_name is None:
        family_name = q.family_name

    if to_unit is None:
        unit_system = _get_unit_system(unit_system)
        try:
            to_unit = unit_system.units(family_name)

        except KeyError:
            logger.exception(
                "Could not convert quantity: %s to system: %s" %
                (q, unit_system))
            return q.clone()

    if q.units == to_unit:
        q = q.clone()

    else:
        data = units_convert(q.data, q.units, to_unit)
        # create a new object of the same type as the input Quantity object
        # could be a subclass, so use __class__
        q = q.__class__(
            data,
            units=to_unit,
            name=q.name or family_name,
            family_name=family_name)
    return q


def _get_unit_system(unit_system=None):
    from scimath.units.unit_manager import unit_manager
    return unit_manager.get_unit_system(unit_system)


def _get_family_name_for_array(units=None):
    from scimath.units.unit_manager import unit_manager
    return unit_manager.get_family_name_for_value(units)


# The dict of defaults
default_unit_converters = {
    "<class 'scimath.units.unit_array.UnitArray'>": convert_unit_array,
    "<class 'scimath.units.quantity.Quantity'>": convert_quantity,
    "<class 'scimath.units.scalar.Scalar'>": convert_quantity,
}
