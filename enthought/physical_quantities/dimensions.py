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
from copy import copy

# Enthought module imports
from enthought.traits.api import HasTraits, String, DictStrFloat, TraitType, \
        Property, cached_property


def dict_mul(a, n):
    """Given a dictionary, multiply values by a scalar
    
    Parameters
    ----------
        a: dict
            the dictionary to be multiplied.
        n: float
            the scalar to multiply by
    
    Example
    -------
    Given a dictionary and scalar:
        
    >>> a = {'a': 2.0, 'b': -4.0}
    >>> n = 1.5
    >>> dict_mul(a, n)
    {'a': 3.0, 'b': -6.0}
    
    """
    if n == 0:
        return {}
    c = copy(a)
    for key in c:
        c[key] *= n
    return c


def dict_div(a, n):
    """Given a dictionary, divide values by a scalar
    
    Parameters
    ----------
        a: dict
            the dictionary to be divided.
        n: float
            the scalar to divide by
    
    Example
    -------
    Given a dictionary and scalar:
        
    >>> a = {'a': 2.0, 'b': -4.0}
    >>> n = 0.5
    >>> dict_div(a, n)
    {'a': 4.0, 'b': -8.0}
    
    """
    c = copy(a)
    for key in c:
        c[key] /= n
    return c


def dict_add(a, b):
    """Given two dictionaries, add values by key, removing zero entries
    
    Parameters
    ----------
        a, b : dict
            the dictionaries to be added.
    
    Example
    -------
    Given two dictionaries:
        
    >>> a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
    >>> b = {'a': 1.5, 'c': 12.0, 'd': -2.0}
    >>> dict_add(a, b)
    {'a': 4.5, 'b': -4.0, 'c': 12.0}
    """
    c = copy(b)
    for key, value in a.items():
        c[key] = value+b.get(key, 0)
        if c[key] == 0.0:
            del c[key]
    return c


def dict_sub(a, b):
    """Given two dictionaries, subtract values by key, removing zero entries
    
    Parameters
    ----------
        a, b : dict
            the dictionaries to be added.
    
    Example
    -------
    Given two dictionaries::
        
    >>> a = {'a': 3.0, 'b': -4.0, 'd': 2.0}
    >>> b = {'a': 1.5, 'c': 12.0, 'd': 2.0}
    >>> dict_sub(a, b)
    {'a': 1.5, 'b': -4.0, 'c': -12.0}
    """
    c = copy(a)
    for key, value in b.items():
        c[key] = a.get(key, 0)-value
        if c[key] == 0.0:
            del c[key]
    return c


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
            return "*".join(key+(("**"+str(value)) if value != 1 else "")
                        for key, value in sorted(self.dimension_dict.items())
                            if value != 0)
        else:
            return "dimensionless"
    
    def __repr__(self):
        return "Dimensions(%s)" % repr(self.dimension_dict)
    
    def __str__(self):
        return self.expansion
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) \
                and self.dimension_dict == other.dimension_dict
       
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
        