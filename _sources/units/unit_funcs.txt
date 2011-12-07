.. _unit-funcs:

Unitted Functions
===============================================================================

A function which handles UnitArrays and UnitScalars is a unitted
function. Unitted functions are created with the
:py:func:`~scimath.units.has_units.has_units` decorator. The units can be
specified by passing arguments to the decorator or by constructing a special
docstring.

   >>> from numpy import array
   >>> from scimath.units.api import has_units
   >>> from scimath.units.length import feet, meter
   >>> @has_units(inputs="a:an array:units=ft;b:array:units=ft",
   ...            outputs="result:an array:units=m")
   ... def add(a,b):
   ...     " Add two arrays in ft and convert them to m. "
   ...     return (a + b) * feet / meter

or, equivalently:

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
   ...     return (a + b) * feet / meter

In the examples above, we told add() to expect two values, ``a`` and ``b`` and
convert them to feet for use in the function. Then we specified that the output
would be in meters. Inside the function, ``a`` and ``b`` are not unitted, and
the function is responsible for the conversion. (Remember our :ref:`caveat
<conversion-factor-caveat>` regarding conversion factors.)

Unitted functions can accept either regular python objects (of the appropriate
type) or the equivalent unitted objects. The return type depends on what it was
passed.

   >>> add(1,2)
   0.9144000000000001

In this case, add() accepted two integer arguments in feet, added them and
returned an integer value in meters.

   >>> add(UnitScalar(1, units="foot"), UnitScalar(2, units="foot"))
   UnitScalar(0.9144000000000001, units='1.0*m')

In this case, add() accepted two UnitScalar arguments in feet and returned a
UnitScalar in pure meters.

   >>> add(UnitScalar(0.5, units="meter"), UnitScalar(50, units="cm"))
   UnitScalar(1.0, units='1.0*m')

Finally, in this case, a conversion to feet was made for the calculation inside
the function, and the value was converted back to meters when returned.

If no units are specified in the outputs, then a regular scalar data type will
be returned.
