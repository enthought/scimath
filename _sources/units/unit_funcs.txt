.. _unit-funcs:

Unitted Functions
===============================================================================

A function which handles UnitArrays and UnitScalars is a unitted
function. Unitted functions are created with the
:py:func:`~scimath.units.has_units.has_units` decorator. The units can be
specified by passing parameters in the decorator or by constructing a special
docstring.::

   >>> from numpy import array
   >>> from scimath.units.api import has_units
   >>> @has_units(inputs="a:an array:units=ft;b:array:units=ft",
   ...            outputs="result:an array:units=m")
   ... def add(a,b):
   ...     " Add two arrays in ft and convert them to m. "
   ...     return (a + b) * 0.3048

or, equivalently: ::

   >>> from scimath.units.api import has_units, UnitArray
   >>> @has_units
   ... def add(a,b):
   ...     ''' Add two arrays in ft and convert them to m.
   ...
   ...         Parameters
   ...         ----------
   ...         a : array : units=ft
   ...             An array
   ...         b : array : units=ft
   ...             Another array
   ...
   ...         Returns
   ...         -------
   ...         c : array : units=m
   ...             c = a + b
   ...     '''
   ...     return (a + b) * 0.3048
