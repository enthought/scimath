#-----------------------------------------------------------------------------
#
#  Copyright (c) 2008 by Enthought, Inc.
#  All rights reserved.
#
#  Author: Corran Webster
#
#-----------------------------------------------------------------------------

"""A class that represents the dimensions of physical quantities

This class provides the Dimensions class which represents an abstract type
for a dimension of a physical quantity such as length, length*mass*time**-2,
currency, etc.
"""

# we don't want integer division when dealing with units
from __future__ import division

# Global module imports

# Enthought module imports
from enthought.traits.api import HasTraits, String, DictStrFloat, TraitType, \
        Property, cached_property

# local imports
from util import dict_mul, dict_div, dict_add, dict_sub, format_expansion



class Dimensions(HasTraits):
    """The dimensions of a physical quantity.
    
    This is essentially a thin wrapper around a dictionary which we perform
    certain operations on.
    
    Example
    -------
    >>> m = Dimensions({'mass': 1.0})
    >>> a = Dimensions({'length': 1.0, 'time': -2.0})
    >>> f = Dimensions({'length': 1.0, 'mass': 1.0, 'time': -2.0})
    >>> f == m*a
    True
    >>> f.expansion
    "length*mass*time**-2.0"
    """

    # a dictionary holding dimension names and quantities
    # this should be frozen if you want to hash - don't change it
    dimension_dict = DictStrFloat
    
    # the quantity type as an expression in powers of base dimensions
    expansion = Property(String, depends_on='dimension_dict')
    
    def __init__(self, dimension_dict, **kwargs):
        for key, value in dimension_dict.items():
            if not value:
                del dimension_dict[key]
        super(self.__class__, self).__init__(dimension_dict=dimension_dict, **kwargs)
    
    @classmethod
    def from_expansion(cls, expansion):
        """Create a Dimension class instance from an expansion string
        
        This is a fairly simplistic parser - no parens, division, etc.
        
        Parameters
        ----------
        expansion : string
            an expansion of the dimensions (eg. mass*length**-3.0)
        """
        terms = expansion.split("*")
        dimension_dict = {}
        try:
            while terms:
                dim = terms.pop(0)
                if terms[0] == "":
                    terms.pop(0)
                    power = float(terms.pop(0))
                    dimension_dict[dim] = dimension_dict.get(dim,0)+power
        except:
            raise InvalidExpansionError(expansion)
        return cls(dimension_dict)
    
    @cached_property
    def _get_expansion(self):
        if self.dimension_dict:
            return format_expansion(self.dimension_dict)
        else:
            return "dimensionless"
    
    def __repr__(self):
        return "Dimensions(%s)" % repr(self.dimension_dict)
    
    def __str__(self):
        return self.expansion
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                and self.dimension_dict == other.dimension_dict
    
    def __hash__(self):
        return hash(tuple(item for item in self.dimension_dict.items()))
       
    def __mul__(self, other):
        if isinstance(other, Dimensions):
            return Dimensions(dict_add(self.dimension_dict,
                                       other.dimension_dict))
        else:
            raise NotImplementedError
    
    def __div__(self, other):
        if isinstance(other, Dimensions):
            return Dimensions(dict_sub(self.dimension_dict,
                                       other.dimension_dict))
        else:
            raise NotImplementedError
    
    def __pow__(self, other):
        if isinstance(other, (float, int, long)):
            return Dimensions(dict_mul(self.dimension_dict, other))
        else:
            raise NotImplementedError


class Dim(TraitType):
    default_value = {}
    info_text = "a dimension information object"
    
    def validate(self, object, name, value):
        if isinstance(value, Dimensions):
            return value
        if isinstance(value, dict):
            return Dimensions(value)
        if isinstance(value, basestring):
            try:
                return Dimensions.from_expansion(value)
            except InvalidExpansionError:
                raise TraitsError
        raise TraitsError


class InvalidExpansionError(ArithmeticError):
    def __init__(self, expansion):
        self.expansion = expansion
        
    def __str__(self):
        return "Invalid expansion: " + repr(self.expansion)
        