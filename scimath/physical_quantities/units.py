"""
"""
# we don't want integer division when dealing with units
from __future__ import division

from __future__ import absolute_import
from numpy import array, log10

from traits.api import HasTraits, Float, String, Unicode, Bool, \
    Dict, Any, Instance, Property, cached_property
#from traitsui.api import View, Item, Group

from .dimensions import Dimensions, Dim


class Unit(HasTraits):
    """ A unit in a measurement system.

    Example
    -------
    >>> N = Unit(name="newton", expression="N", dimensions=Force,
                    scale=1.0)
    >>> dyn = Unit(name="dyne", expression="dyn", dimensions=Force,
                    scale=0.00001)
    >>> converter = N.make_converter(dyne)
    >>> converter(10)
    1000000.0
    """

    # a symbolic expression for the unit
    symbol = Unicode

    # a python expression which can evaluate to this unit
    expression = String

    # a LaTeX string holding an expression for the unit
    latex = String

    # a dictionary holding dimension names and quantities
    dimensions = Dim

    scale = Float(1.0)
    offset = Float(0.0)
    logarithmic = Bool(False)
    log_base = Float(10.0)

    def convert_to_base(self, x):
        """ Convert a numeric value to base units

            This converts a numeric value to the base units of the Unit's
            dimensions.  For example, in an SI-base system, Units whose
            dimensions are Length would be converted to a value in metres.

            Parameters
            ----------
            x : Any
                the value that will be converted

            Results
            -------
            y : Any
                the value in the base units
        """
        if self.logarithmic:
            return self.log_base**(x / self.scale + self.offset)
        else:
            return x / self.scale + self.offset

    def convert_from_base(self, x):
        """ Convert a value from base units

            This converts a value from the base units of the Unit's
            dimensions.  For example, in an SI-base system, Units whose
            dimensions is Length would be converted from metres.

            Parameters
            ----------
            x : Any
                the value that will be converted from base units

            Results
            -------
            y : Any
                the value in this set of units
        """
        if self.logarithmic:
            return self.scale * (log10(x) / log10(self.log_base) - self.offset)
        else:
            return self.scale * (x - self.offset)

    def convert_to_unit(self, x, unit):
        """ Convert a value to compatible units

            This converts a value in these units to ``unit`` units, as long as
            the units have compatible dimensions.

            Defaults to converting to base units and then from base units.
            This should be overridden by sub-classes for performance reasons.

            Parameters
            ----------
            x : Any
                the value that will be converted
        """
        if self.dimensions != unit.dimensions:
            raise QuantityTypeError(self.dimensions, unit.dimensions)
        return unit.convert_from_base(self.convert_to_base(x))

    def convert_from_unit(self, x, unit):
        """ Convert a value to compatible units

            This converts a value in these units to ``unit`` units, as long as
            the units have compatible dimensions.

            Defaults to converting to base units and then from base units.
            This should be overridden by sub-classes for performance reasons.

            Parameters
            ----------
            x : Any
                the value that will be converted
        """
        if self.dimensions != unit.dimensions:
            raise QuantityTypeError(self.dimensions, unit.dimensions)
        return self.convert_from_base(unit.convert_to_base(x))

    def make_converter(self, unit):
        """ Return a function that converts this unit to the specified unit.

            Parameters
            ----------
            unit : Unit
                the desired units to convert to
        """
        if self.dimensions != unit.dimensions:
            raise QuantityTypeError(self.dimensions, unit.dimensions)
        return lambda x: self.convert_to_unit(x, unit)

    def __eq__(self, other):
        return isinstance(other, Unit) \
            and self.dimensions == other.dimensions \
            and self.scale == other.scale \
            and self.offset == other.offset \
            and self.logarithmic == other.logarithmic \
            and (not self.logarithmic or self.log_base == other.log_base)

    def __hash__(self):
        return hash((tuple(item for item in self.dimensions.dimension_dict.items()),
                     self.scale, self.offset, self.logarithmic, self.log_base))

    def __mul__(self, other):
        if isinstance(other, (float, int, int, array)):
            return Quantity(magnitude=other, units=self)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        if isinstance(other, (float, int, int, array)):
            return Quantity(magnitude=other, units=self)
        else:
            raise NotImplementedError

    def __div__(self, other):
        return type(self).__truediv__(self, other)

    def __truediv__(self, other):
        if isinstance(other, (float, int, array)):
            return Quantity(magnitude=1.0/other, units=self)
        else:
            raise NotImplementedError


class MultiplicativeUnit(Unit):
    """ A multiplicative unit in a measurement system.

    Example
    -------
    >>> N = MultiplicativeUnit(name="newton", expression="N",
                    dimensions=Force, scale=1.0)
    >>> dyn = MultiplicativeUnit(name="dyne", expression="dyn",
                    dimensions=Force, scale=0.00001)
    >>> converter = N.make_converter(dyne)
    >>> converter(10)
    1000000.0
    """

    derivation = Dict

    def convert_to_base(self, x):
        return x / self.scale

    def convert_from_base(self, x):
        return x * self.scale

    def make_converter(self, other):
        """Return a function which converts from self to other.
        """
        if isinstance(other, MultiplicativeUnit):
            return lambda x: x * (other.scale / self.scale)
        else:
            return super(MultiplicativeUnit, self).make_converter(other)

    def __mul__(self, other):
        if isinstance(other, MultiplicativeUnit):
            return DerivedUnit(derivation=dict_add(self.derivation,
                                                   other.derivation),
                               scale=self.scale * other.scale)
        else:
            raise NotImplementedError

    def __div__(self, other):
        return type(self).__truediv__(self, other)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return DerivedUnit(derivation=dict_sub(self.derivation,
                                                   other.derivation),
                               scale=self.scale / other.scale)
        else:
            raise NotImplementedError

    def __pow__(self, other):
        if isinstance(other, (float, int, int)):
            return DerivedUnit(derivation=dict_mul(self.derivation,
                                                   other.derivation),
                               scale=self.scale**other)
        else:
            raise NotImplementedError


class DerivedUnit(MultiplicativeUnit):
    # a name for the unit
    name = Property(String, depends_on="derivation")

    # a symbolic expression for the unit
    symbol = Property(Unicode, depends_on="derivation")

    # a python expression which can evaluate to this unit
    expression = Property(String, depends_on="derivation")

    # a LaTeX string holding an expression for the unit
    latex = Property(String, depends_on="derivation")

    # a dictionary holding dimension names and quantities
    dimensions = Property(Dim, depends_on="derivation")

    @cached_property
    def get_symbol(self):
        return format_expansion(dict((key.symbol, power)
                                     for key, power in self.derivation.items()),
                                mul=" ", pow_func=unicode_power, div=True)

    @cached_property
    def get_expression(self):
        return format_expansion(dict((key.expression, power)
                                     for key, power in self.derivation.items()))

    @cached_property
    def get_dimensions(self):
        dim = dimensionless
        for key, power in self.derivation.items():
            dim *= key.dimensions**power
        return dim


class NamedUnit(MultiplicativeUnit):

    def __init__(self, **kw):
        kw['derivation'] = {self: 1.0}
        super(NamedUnit, self).__init__(**kw)


class BaseUnit(NamedUnit):

    def convert_to_base(self, x):
        return x * self.scale

    def convert_from_base(self, x):
        return x / self.scale
