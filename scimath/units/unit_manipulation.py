# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Methods to handle unit conversion into/outoff function components.

    Component decorators wrap standard python functions with "conversion"
    routines that can either change or add information to functions before
    the actual python function call is made.  A standard need for this is
    unit conversion.  There are a couple of common cases that we run into
    in scientific applications.  The first is that we want to take objects
    that have one set of units and convert their data to another set of units
    before handing them into the function.  This is important if a function
    was written expecting data in a specific set of units (ie. m/s instead
    of ft/s).  convert_units() does this as well as adding units to non-united
    objects.  On output, it is common to want to take objects that may not
    have units associated with them and convert them to a 'united' object
    that has units associated with them set_units() does this.
"""

# Numeric library imports
from numpy import ndarray

# Enthought library imports
import scimath.units as units

# Numerical modeling library imports
from scimath.units.unit_array import UnitArray
from scimath.units.unit_scalar import UnitScalar


def manipulate_units(units, converters, *args):
    """ Convert the \*args to the specified units using the converters.

        This function is general purpose in that it could do a unit conversion,
        it could overwrite the objects' units, or whatever. The behavior is up
        to the converter functions.

        Parameters
        ----------
        units
            A sequence of unit objects the same length as \*args, where
            ``units[n]`` is the new units for ``args[n]``.
        converters
            A dictionary of conversion functions with (type, func(val, unit)).
        \*args
            List of variables to be converted.

        Returns
        -------
        results
            List cooresponding to \*args of converted values.

    """
    # fixme:  I haven't thought about flexibility much yet.
    #        We might want to be able to change this method out during
    #        execution.  We also might want to be able to swap out
    #        converters.  Further, a specific method might want to have its
    #        own conversion method?

    # fixme: We likely want some logging options here so that we can report
    #       to users what unit conversions are happening.

    # Ensure there are units for each argument.
    if len(units) != len(args):
        msg = 'There must be a unit definition for each argument (%d!=%d)' % \
            (len(units), len(args))
        raise ValueError(msg)

    results = []
    for value, unit in zip(args, units):
        if unit is None:
            results.append(value)
        else:
            try:
                # Use an exact match for the converter, if we can
                results.append(converters[type(value)](value, unit))
            except KeyError:
                # Loop through converters and see if there is one that is
                # base class of this type.  If so, we'll use that.
                for type_, convert in converters.items():
                    if isinstance(value, type_):
                        results.append(convert(value, unit))
                        converters[type(value)] = convert  # (Cache)
                        break
                else:
                    results.append(value)

    # Unwrap if there is only one of them
    if len(results) == 1:
        results = results[0]

    return results


def convert_units(units, *args):
    converters = {
        # UnitScalar: ... # 'UnitScalar' is a subtype of 'UnitArray'
        UnitArray: unit_array_units_converter,
    }
    return manipulate_units(units, converters, *args)


def set_units(units, *args):
    converters = {
        float: scalar_to_unit_scalar_converter,
        int: scalar_to_unit_scalar_converter,
        ndarray: array_to_unit_array_converter,
        UnitArray: unit_array_units_overwriter,
    }
    return manipulate_units(units, converters, *args)


def have_some_units(*args):
    """ Returns True if any of the arguments have units attached to them.

    This is a bit of a hack specifically for has_units and tied to the
    conventions of convert_units().
    """
    for arg in args:
        if isinstance(arg, UnitArray):
            return True
    return False


def strip_units(*args):
    """ Remove units from arguments.
    """
    ret = []
    for arg in args:
        if isinstance(arg, UnitArray):
            # This also takes care of UnitScalars as a subclass.
            ret.append(arg.view(ndarray))
        else:
            ret.append(arg)
    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)

# Convert objects with units to the same type of object with new units.


def unit_array_units_converter(unit_array, new_units):
    """ Convert a UnitArray from one set of units to another.
    """
    if unit_array.units != new_units:
        # Need conversion.
        if isinstance(unit_array, ndarray) and unit_array.shape != ():
            # this is an array
            result = UnitArray(units.convert(unit_array.view(ndarray), unit_array.units,
                                             new_units))
        else:
            # this is a scalar
            result = UnitScalar(units.convert(unit_array.view(ndarray), unit_array.units,
                                              new_units))
        result.units = new_units
    else:
        # No conversion needed.  Just return the unit_array.
        result = unit_array

    return result


# These two functions don't really do unit conversion.  Rather, they add units
# to objects that don't have them.  This often involves converting them to a
# new type of object.

def scalar_to_unit_scalar_converter(x, units):
    """ Create a UnitScalar with units='units' from the given scalar 'x'.
    """

    return UnitScalar(x, units=units)


def array_to_unit_array_converter(array, units):
    """ Create a UnitArray with units='units' from the given 'array'.
    """
    if array.shape == ():
        return UnitScalar(array, units=units)
    return UnitArray(array, units=units)


# *Overwrite* the existing units on an object with new units.  No unit
# conversion takes place.
def unit_array_units_overwriter(unit_array, new_units):
    """ Overwrite the units for a UnitArray with the new units.
    """

    if not hasattr(unit_array, 'units') or unit_array.units != new_units:
        unit_array.units = new_units

    return unit_array
