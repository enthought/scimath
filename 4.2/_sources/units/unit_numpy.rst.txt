.. _units-with-numpy:

===============================================================================
Units with Numpy
===============================================================================

For high-performance computation, Scimath.units includes two objects for adding
units to `Numpy`_ `ndarray`_ objects: the
:py:class:`~scimath.units.unit_scalar.UnitScalar` and the
:py:class:`~scimath.units.unit_scalar.UnitArray`. UnitScalars and UnitArrays
can be used directly in computations but are best handled with :ref:`unitted
functions<unit-funcs>` constructed using the
:py:func:`~scimath.units.has_units.has_units` decorator.

.. _working-with-unit-scalars:

Working with UnitScalars and UnitArrays
===============================================================================

UnitScalar example
------------------

As a basic example using scalar values, let's create two UnitScalars and add
them. Say we were averaging the wing spans of African swallows (a) with
that of European swallows (e).

 >>> from scimath.units.api import UnitScalar
 >>> a = UnitScalar(5, units="inches")
 >>> e = UnitScalar(15, units="cm")
 >>> (a + e) / 2
 UnitScalar(5.452755905511811, units='0.025400000000000002*m')

Note that the result is a UnitScalar whose default units are *inches*, but it
displays as a derivation from the SI fundamental unit *meters*. This is because
UnitScalar values are stored internally as derivations of the SI system, thus
if the value is assigned in a non-SI unit, part of the value may appear in the
units. (See the section on :ref:`internal representation
<internal-representation>` for more detail.)

 >>> UnitScalar(1, units="inch")
 UnitScalar(1, units='0.025400000000000002*m')

A UnitScalar assumes the units that are first assigned to it. From the example
above,

 >>> (e + a) / 2
 UnitScalar(13.85, units='0.01*m')

This does not fundamentally change the value of the variable, but it can lead
to rounding errors and unexpected results:

 >>> (e + a) == (a + e)
 UnitScalar(False, units='None')

since

 >>> (a + e) - (e + a)
 UnitScalar(1.7763568394002505e-15, units='0.025400000000000002*m') 

which is awfully close but not quite equal to zero.

UnitArray example
-----------------

A UnitArray uses a Numpy ndarray  as its value.

 >>> from numpy import linspace
 >>> a = UnitArray(linspace(0, 5, 6), units="cm")
 >>> a
 UnitArray([ 0.,  1.,  2.,  3.,  4.,  5.], units='0.01*m')

UnitArrays can be multiplied by UnitScalars or other UnitArrays, as in NumPy.::

   >>> a * b
   UnitArray([0.,  1.,  2.,  3.,  4.,  5.], units='0.0030480000000000004*m**2')

Note that part of the value is contained in the unit string.

For high-performance computation with UnitArrays use :ref:`unitted functions
<unit-funcs>`.


.. _NumPy: http://www.numpy.org
.. _ndarray: http://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html
