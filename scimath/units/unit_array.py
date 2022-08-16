# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Numeric Library Imports
import numpy

# Enthought library imports
from scimath.units import convert
from scimath.units.unit import unit, dimensionless, IncompatibleUnits
from scimath.units.unit_parser import unit_parser


def __newobj__(cls, *args):
    """ Unpickles new-style objects.
    """
    return cls.__new__(cls, *args)


_retain_units = [numpy.absolute, numpy.negative,
                 numpy.floor, numpy.ceil, numpy.rint, numpy.conjugate,
                 numpy.maximum, numpy.minimum]

_retain_units_if_same = []  # [numpy.add, numpy.subtract]

_retain_units_if_single = []  # [numpy.multiply]

_retain_units_if_only_first = [numpy.remainder]  # , numpy.divide]


class UnitArray(numpy.ndarray):
    """ Define a UnitArray that subclasses from a Numpy array

        This class simply adds a "units" object to a numpy array.  It deals
        with unit adjustments involving basic arithmetic and comparison
        operations between arrays with units.  If incompatible units are
        used, an error will be raised.

        Note that the "units" may hold some amount of the magnitude, which can
        be particularly significant for dimensionless quantities.

        You should always convert a UnitArray to the required units before
        extracting the numerical value.

        This code is shamelessly copied from the numpy matrix class.  It is
        of course modified to suite our purposes.
    """

    ##########################################################################
    # numpy.ndarray attributes
    ##########################################################################

    # priority->0.0 results in binary array ops returning UnitArray objects.
    __array_priority__ = 10.0

    ##########################################################################
    # UnitArray attributes
    #
    # Note: These are commented out because we are not using traits.  However,
    #       They are left here for documentation.
    ##########################################################################

    # Units specification.  it is a scimath.units.unit object, not a string.
    # units = Instance(unit)

    # 'type' specifies the type of UnitArray.
    # This could be useful for specifying that this is a 'tops' UnitArray or of
    # 'flag' or other such types.  I am not sure if this is useful, but I
    # think it might be.
    # fixme: Not Implemented
    # type = Str

    ##########################################################################
    # object interface
    ##########################################################################
    def __repr__(self):
        """ String representation using the repr of the unit."""
        base_str = self._get_values_base_str()
        s = "{klass}({val}, units='{unit!r}')"
        klass = type(self).__name__
        return s.format(klass=klass, val=base_str, unit=self.units)

    def __str__(self):
        """ String representation using the label of the unit."""
        s = "{klass} ({unit}): {val}"
        base_str = self._get_values_base_str()
        if self.units.label is not None:
            str_unit = self.units.label
        else:
            str_unit = repr(self.units)

        return s.format(klass=type(self).__name__, val=base_str, unit=str_unit)

    def __reduce_ex__(self, protocol):
        """
        pickling function for classes which inherit from tuple.

        __reduce_ex__ must be overloaded for pickling to work. Refer to the docs
        in the pickle source code for details as to why.

        """

        state = (self.units, super(UnitArray, self).__reduce_ex__(protocol))
        return (__newobj__, (self.__class__, ()), state)

    def __setstate__(self, state):
        """
        unpickling function
        """

        super(UnitArray, self).__setstate__(state[1][2])
        units = state[0]
        self.units = units

    def __deepcopy__(self, memo={}):
        copy = self.__class__(self.view(numpy.ndarray), copy=True,
                              units=self.units)
        memo[id(self)] = copy
        return copy

    ##########################################################################
    # numpy.ndarray interface
    ##########################################################################

    def __new__(cls, data, dtype=None, copy=True, units=None):
        """ Called when a new object is created (before __init__).

            The default behavior of ndarray is overridden to add units and
            family_name to the class.

            For more details, see:
                http://docs.python.org/ref/customization.html

        """

        ### Array Setup #######################################################

        if isinstance(data, numpy.ndarray):
            # Handle the case where we are passed in a numpy array.
            if dtype is None:
                intype = data.dtype
            else:
                intype = numpy.dtype(dtype)

            new = data.view(cls)

            if intype != data.dtype:
                res = new.astype(intype)
            elif copy:
                res = new.copy()
            else:
                res = new

        else:
            # Handle other input types (lists, etc.)
            arr = numpy.array(data, dtype=dtype, copy=copy)

            res = numpy.ndarray.__new__(cls, arr.shape, arr.dtype,
                                        buffer=arr)

        ### Configure Other Attributes ########################################
        if isinstance(units, str):
            units = unit_parser.parse_unit(units)

        res.units = units

        return res

    def __array_finalize__(self, obj):
        """
        Copy any values that were on the original UnitArray into the output
        UnitArray.
        """
        units = getattr(obj, 'units', None)
        self.units = units

    def __array_wrap__(self, obj, context=None):
        # Behavior of getting units is
        #   to retain units if
        #  1) the function is in _retain_units list
        #  2) the function is in _retain_units_if_same list
        #     and the arguments either have the same units
        #     or no units.
        #  3) the function is in _retain_units_if_single list
        #     and all but one argument does not have units
        #     (or is dimensionless)
        #  4) the function is in _retain_units_if_only_first
        #     and all but the first argument does not have units
        #     (or is dimensionless)
        #  5) the function has a single argument which is dimensionless
        #
        # FIXME: To do this "right" would require a ufunc
        #      object that could tell how to do unit conversions
        #      with its inputs to produce its outputs.
        result = obj.view(self.__class__)
        theunit = None
        if context is not None:
            func, args, iout = context
            if func in _retain_units:
                theunit = getattr(self, 'units', None)
            elif func in _retain_units_if_same:
                theunit = None
                for arg in args:
                    u = getattr(arg, 'units', None)
                    if u is None:
                        continue
                    if theunit is None:
                        theunit = u
                    elif (theunit != u):
                        theunit = None
            elif func in _retain_units_if_single:
                theunit = None
                for arg in args:
                    u = getattr(arg, 'units', None)
                    if u is not None:
                        if theunit is None:
                            theunit = u
                        elif u != dimensionless:  # already a unit
                            theunit = None
                            break
            elif func in _retain_units_if_only_first:
                theunit = getattr(args[0], 'units', None)
                for arg in args[1:]:
                    u = getattr(arg, 'units', None)
                    if u is not None and u != dimensionless:
                        theunit = None
                        break
            elif len(args) == 1:
                theunit = getattr(self, 'units', None)
                if theunit != dimensionless:
                    theunit = None

        result.units = theunit
        return result

    def __convert_other(self, other):
        su = getattr(self, 'units', dimensionless)
        ou = getattr(other, 'units', dimensionless)

        if su is None and ou is None:
            u = None
        else:
            if isinstance(other, unit):
                # Handles 5 * liters
                ou = unit(1, other.derivation)
                other = convert(other.value, ou, su)
            elif isinstance(other, UnitArray):
                # Handles UnitArray or UnitScalar
                other = convert(numpy.array(other), ou, su)
            elif isinstance(other, numpy.ndarray):
                if len(other.shape) > 0 and hasattr(
                        other.item(0), 'derivation'):
                    # Handles array([1,2,3] * liters)
                    ou = unit(1, other.item(0).derivation)
                    other = convert(other / ou, ou, su)
            u = su
        return other, u

    def __add__(self, other):
        """
        Defines the addition of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__add__(other)
        result.units = u
        return result

    def __radd__(self, other):
        """
        Defines the reverse addition of 2 unitted arrays
        """
        # Addition is commutative
        return self.__add__(other)

    def __sub__(self, other):
        """
        Defines the subtraction of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__sub__(other)
        result.units = u
        return result

    def __rsub__(self, other):
        """
        Defines the reverse subtraction of 2 unitted arrays
        """
        su = getattr(self, 'units', dimensionless)
        ou = getattr(other, 'units', dimensionless)
        if su is None and ou is None:
            s = self
            u = None
        else:
            s = self.as_units(ou)
            u = ou
        result = super(UnitArray, s).__rsub__(other)
        result.units = u
        return result

    def __mul__(self, other):
        """
        Defines the multiplication of 2 unitted arrays
        """
        result = super(UnitArray, self).__mul__(other)
        su = getattr(self, 'units', None)
        ou = getattr(other, 'units', None)
        if su and ou:
            # note that there may be a scale factor in the units.
            # This may be confusing for otherwise dimensionless
            # quantities
            result.units = su * ou
        elif su:
            result.units = su
        else:
            result.units = ou

        # If the units are only a scale factor, apply it to result and set
        # to dimensionless
        if isinstance(result.units, float):
            result = result.as_units(dimensionless)
        return result

    def __rmul__(self, other):
        """
        Defines the reverse multiplication of 2 unitted arrays
        """
        # multiplication is commutative
        return self.__mul__(other)

    def __div__(self, other):
        return type(self).__truediv__(self, other)

    def __truediv__(self, other):
        """
        Defines the division of 2 unitted arrays
        """
        result = super(UnitArray, self).__truediv__(other)
        su = getattr(self, 'units', None)
        ou = getattr(other, 'units', None)
        if su and ou:
            # note that there may be a scale factor in the units.
            # This may be confusing for otherwise dimensionless
            # quantities, but the alternative is losing units like
            # 'percent'
            result.units = su / ou
        elif ou:
            result.units = 1 / ou
        else:
            result.units = su

        # If the units are only a scale factor, apply it to result and set
        # to dimensionless
        if isinstance(result.units, float):
            result = result.as_units(dimensionless)
        return result

    def __rdiv__(self, other):
        return type(self).__rtruediv__(self, other)

    def __rtruediv__(self, other):
        """
        Defines the reverse division of 2 unitted arrays
        """
        result = super(UnitArray, self).__rtruediv__(other)
        su = getattr(self, 'units', None)
        ou = getattr(other, 'units', None)
        if su and ou:
            # note that there may be a scale factor in the units.
            # This may be confusing for otherwise dimensionless
            # quantities
            result.units = ou / su
        elif su:
            result.units = 1 / su
        else:
            result.units = ou

        # If the units are only a scale factor, apply it to result and set
        # to dimensionless
        if isinstance(result.units, float):
            result = result.as_units(dimensionless)
        return result

    def __pow__(self, other):
        """
        Defines the exponent operator of a unitted array
        """
        if isinstance(other, (int, int, float)) or \
                (isinstance(other, numpy.ndarray) and other.shape == ()):
            if isinstance(other, UnitArray):
                if getattr(other, "units", dimensionless) == dimensionless:
                    other = float(other)
                else:
                    raise IncompatibleUnits("exponent must be dimensionless")
            result = super(UnitArray, self).__pow__(other)
            su = getattr(self, 'units', None)
            if su is not None:
                result.units = su**other
            return result
        else:
            raise TypeError("exponent must be an integer, float or 0-d array")

    def __rpow__(self, other):
        return NotImplemented

    def __le__(self, other):
        """
        Defines the 'less or equal' operator of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__le__(other)
        return result

    def __lt__(self, other):
        """
        Defines the 'less than' operator of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__lt__(other)
        return result

    def __ge__(self, other):
        """
        Defines the 'greater or equal' operator of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__ge__(other)
        return result

    def __gt__(self, other):
        """
        Defines the 'greater than' operator of 2 unitted arrays
        """
        other, u = self.__convert_other(other)
        result = super(UnitArray, self).__gt__(other)
        return result

    def __eq__(self, other):
        """
        Defines the 'equal' operator of 2 unitted arrays
        """
        try:
            other, u = self.__convert_other(other)
            result = super(UnitArray, self).__eq__(other)
            return result
        except:
            return False

    def __ne__(self, other):
        """
        Defines the 'not equal' operator of 2 unitted arrays
        """
        try:
            other, u = self.__convert_other(other)
            result = super(UnitArray, self).__ne__(other)
            return result
        except:
            return True

    ##########################################################################
    # UnitArray interface
    ##########################################################################

    ### Unit Conversion ######################################################

    def as_units(self, new_units):
        """ Convert UnitArray from its current units to a new set of units.

        """
        result = self.__class__(convert(self.view(numpy.ndarray),
                                        self.units, new_units))
        result.units = new_units

        return result

    # Unit Conversion ########################################################

    def _get_values_base_str(self):
        """ Build a string representation of the array values.
        """
        # this is a little more complicated than it should be in order
        # to be more resilient to changes to numpy ndarray API
        base_str = numpy.ndarray.__repr__(self.view(numpy.ndarray))
        start = base_str.find('(')
        end = base_str.rfind(')')

        if start > -1 and end > -1:
            base_str = base_str[start+1:end]

        return base_str

    ##########################################################################
    # static methods which wrap numpy builtin functions
    ##########################################################################

    @staticmethod
    def concatenate(sequences, axis=0):
        result = numpy.concatenate(sequences, axis)
        result.units = sequences[0].units
        return result
