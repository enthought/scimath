# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2003  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import operator

import numpy


class unit(object):

    _labels = ('m', 'kg', 's', 'A', 'K', 'mol', 'cd')
    _zero = (0,) * len(_labels)
    _negativeOne = (-1, ) * len(_labels)

    def __init__(self, value, derivation, offset=0.0):
        self.value = value
        self.derivation = derivation
        self.label = None
        self.offset = offset

    def __eq__(self, other):
        """ Are these the same types of units (e.g., feet) """
        # TODO: this comparison does not work for temperature
        if self is other:
            return True

        if not isinstance(other, unit):
            return False

        return self.value == other.value and \
            self.derivation == other.derivation and \
            self.offset == other.offset

    def __ne__(self, other):

        if self is other:
            return False

        if not isinstance(other, unit):
            return True

        return self.value != other.value or \
            self.derivation != other.derivation or\
            self.offset != other.offset

    def __hash__(self):
        return hash(("scimath.unit", self.value, self.derivation, self.offset))

    def __add__(self, other):
        if not self.derivation == other.derivation:
            raise IncompatibleUnits("add", self, other)

        return unit(self.value + other.value, self.derivation)

    def __sub__(self, other):
        if not self.derivation == other.derivation:
            raise IncompatibleUnits("subtract", self, other)

        return unit(self.value - other.value, self.derivation)

    def __mul__(self, other):
        if self._compatibleNumericType(other):
            return unit(other * self.value, self.derivation)

        value = self.value * other.value
        derivation = tuple(
            map(operator.add, self.derivation, other.derivation))

        if derivation == self._zero:
            return value

        return unit(value, derivation)

    def __div__(self, other):
        return type(self).__truediv__(self, other)

    def __truediv__(self, other):
        if self._compatibleNumericType(other):
            return unit(self.value / other, self.derivation)

        value = self.value / other.value
        derivation = tuple(
            map(operator.sub, self.derivation, other.derivation))

        if derivation == self._zero:
            return value

        return unit(value, derivation)

    def __pow__(self, other):
        if not self._compatibleNumericType(other):
            raise InvalidOperation("**", self, other)

        value = self.value ** other
        derivation = tuple(map(operator.mul, [other] * 7, self.derivation))

        return unit(value, derivation)

    def __pos__(self): return self

    # TODO: I don't think these will work for derived classes...
    def __neg__(self): return unit(-self.value, self.derivation)

    def __abs__(self): return unit(abs(self.value), self.derivation)

    def __invert__(self):
        value = 1. / self.value
        derivation = tuple(
            map(operator.mul, self._negativeOne, self.derivation))
        return unit(value, derivation)

    def __rmul__(self, other):
        if not self._compatibleNumericType(other):
            raise InvalidOperation("*", other, self)

        return unit(other * self.value, self.derivation)

    def __rdiv__(self, other):
        return type(self).__rtruediv__(self, other)

    def __rtruediv__(self, other):
        if not self._compatibleNumericType(other):
            raise InvalidOperation("/", other, self)

        value = other / self.value
        derivation = tuple(
            map(operator.mul, self._negativeOne, self.derivation))

        return unit(value, derivation)

    def __float__(self):
        if self.derivation == self._zero:
            return float(self.value)
        raise InvalidConversion(self)

    def __str__(self):
        """ Return the pretty units label if it exists.
        """
        if isinstance(self.value, numpy.ndarray):
            st = "<array>"
        else:
            st = str(self.value)
        derivation = self._strDerivation()
        if not derivation:
            return st

        # Only include the offset if it is nonzero. Unfortunately, this will
        # not be parseable because you cannot add offsets to units by addition.
        string = st + "*" + derivation
        if self.offset:
            string += "+" + str(self.offset)

        return string

    # TODO: something's broken here, I think...perhaps a rename is needed for
    # _strDerivation either here or in the helper function.
    def __repr__(self):
        """ Returns the raw SI units. E.g., g/cc would be 1000 kg \* m \*\*-3.
        """
        if isinstance(self.value, numpy.ndarray):
            st = "<array>"
        else:
            st = repr(self.value)
        derivation = self._strDerivation()
        if not derivation:
            return st

        # Only include the offset if it is nonzero. Unfortunately, this will
        # not be parseable because you cannot add offsets to units by addition.
        string = st + "*" + derivation
        if self.offset:
            string += "+" + repr(self.offset)

        return string

    def _strDerivation(self):
        return _strDerivation(self._labels, self.derivation)

    def _compatibleNumericType(self, other):
        return (isinstance(other, type(0)) or isinstance(other, type(0.0)) or
                isinstance(other, numpy.ndarray))

# instances

one = dimensionless = unit(1, unit._zero)
dim = none = dimensionless  # TODO: does it make any sense to assign 'none'
                      #       as a variable? ...not a very good name
dimensionless.label = "dimensionless"

# helpers


def _strDerivation(labels, exponents):
    dimensions = [_f for _f in map(_strUnit, labels, exponents) if _f]
    return "*".join(dimensions)


def _strUnit(label, exponent):
    if exponent == 0:
        return None
    if exponent == 1:
        return label
    return label + "**%g" % exponent


# exceptions

class InvalidConversion(Exception):

    def __init__(self, operand):
        self._op = operand

    def __str__(self):
        str = "dimensional quantities ('%s') " % self._op._strDerivation()
        str = str + "cannot be converted to scalars"
        return str


class InvalidOperation(Exception):

    def __init__(self, op, operand1, operand2):
        self._op = op
        self._op1 = operand1
        self._op2 = operand2

    def __str__(self):
        str = "Invalid expression: %s %s %s" % (self._op1, self._op, self._op2)
        return str


class IncompatibleUnits(Exception):

    def __init__(self, op, operand1, operand2):
        self._op = op
        self._op1 = operand1
        self._op2 = operand2

    def __str__(self):
        str = "Cannot %s quantities with units of '%s' and '%s'" % \
              (self._op, self._op1._strDerivation(), self._op2._strDerivation())
        return str


def is_dimensionless(unit):
    """ Determines whether a unit is dimensionless, i.e., has no units.
    """
    if unit.derivation == dimensionless.derivation:
        return True

    return False
