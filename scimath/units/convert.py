# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines the convert, convert_str and parser function
"""

import numpy
from .unit import InvalidConversion


#####################################################################
# Definitions:
#####################################################################

def convert(value, from_unit, to_unit):
    """ Coverts value from one unit to another.

    Parameters
    ----------
    value : float
        value to convert
    from_unit : scimath.unit object
        implied units of 'value'
    to_unit : scimath.unit object
        implied units of the returned float

    Returns
    -------
    value * conversion_factor + offset : data type is the same as was passed
    in.

    Description
    -----------

    Checks first to see if from_unit and to_unit are equal and passes value
    back in that case. Then convert() forms a conversion factor by dividing the
    units. The offset is zero unless explicitly set otherwise in the unit
    definition. Handling of UnitArrays is done by checking whether value is a
    numpy.ndarray.

    **Note**: Enthought has extended the original units implementation to
    handle temperature conversions.  Temperature units are a special case
    because they can have a different origin.

    This causes a fundamental ambiguity. What behavior do we expect when we
    convert temperature?

    Option #1 When we convert 0 degrees centigrade we get 32 fahrenheit.

    Option #2 When we convert a temperature difference of 0 degrees centigrade
    we get a temperature difference of 0 degrees fahrenheit.

    By convention we have made the units system behave like in Option
    #1 so that convert() handles absolute temperatures, not temperature
    differences.
    """

    # TODO: it would be nice if this function could handle inversion as well as
    # just scaling and also gave better error messages. For example:
    '''
    res = from_unit / to_unit

    if  from_unit / to_unit is dimensionless:
        # straight convert\
        pass
    elif  from_unit * to_unit is dimensionless:
        # invert
        pass
    else:
        # dimensionally incompatible
        pass
    '''

    # TODO: This is my guess at what Lowell did to improve performance...
    # I need to confirm that I'm doing the same thing he did (TNV)

    if from_unit == to_unit:
        return value
    else:
        try:
            # try a straight conversion
            factor = float(from_unit / to_unit)
        except InvalidConversion as ex:
            # try an inversion
            factor = from_unit * to_unit
            if not isinstance(factor, float):
                raise ex
        try:
            offset = (from_unit.offset * factor) - to_unit.offset
        except AttributeError:
            offset = 0.0

    # test if it is a UnitArray without importing UnitArray to keep
    # the dependencies low for this module
    if isinstance(value, numpy.ndarray) and hasattr(value, 'units'):
        return value * factor + value.units * offset

    return value * factor + offset


def convert_str(value, from_unit_string, to_unit_string):
    """ Convert functions to take in strings and conveniently parse them to
        units, to return the conversion factor

        Parameters
        ----------
        from_unit_string: Str
            String representing from_unit, eg. 'm'
        to_unit_string: Str
            String representing to_unit, eg. 'ft'

        Returns:
        --------
        return_value: Float
            Conversion factor between the from_unit and the to_unit
    """
    from scimath.units import unit_parser
    return convert(value,
                   unit_parser.unit_parser.parse_unit(from_unit_string),
                   unit_parser.unit_parser.parse_unit(to_unit_string))


# Function to return a parser instance

def parser():
    from scimath.units import unit_parser
    return unit_parser.unit_parser()
