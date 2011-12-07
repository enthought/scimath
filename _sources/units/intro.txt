===============================================================================
Introduction to SciMath Units
===============================================================================

Scimath units is a system for adding units to `Numpy`_ `ndarray`_ objects. The
primary data types of scimath.units are the
:py:class:`~scimath.units.unit_scalar.UnitScalar` and the
:py:class:`~scimath.units.unit_scalar.UnitArray`. UnitScalars and UnitArrays
are handled with unitted functions constructed using the
:py:func:`~scimath.units.has_units.has_units` decorator.

A large number of units used in science and engineering are available for use,
and scimath.units makes converting among them easy.


Getting Started
===============================================================================
As a basic example, let's create two UnitScalars and multiply them.::

    >>> from scimath.units.api import UnitScalar
    >>> a = UnitScalar(0.5, units="meter")
    >>> b = UnitScalar(1, units="feet")
    >>> c = a + b
    >>> c
    UnitScalar(0.8048, units='1.0*m')

Note that the result ``c`` is a UnitScalar whose default units are *meters*.
UnitScalar values are stored internally in the SI system, although if the value
is assigned in a non-SI unit, part of the value may appear in the units.::

   >>> d = UnitScalar(2, units="inch")
   >>> d
   UnitScalar(2, units='0.025400000000000002*m')

A UnitScalar takes on the default units that are first assigned to it. From the
example above,::

   >>> e = b + a
   >>> e
   UnitScalar(2.6404199475065617, units='0.3048*m')

This does not fundamentally change the value of the variable, but it can lead
to rounding errors::

   >>> d == e
   UnitScalar(False, units='None')

since::

   >>> c - e
   UnitScalar(-1.1102230246251565e-16, units='1.0*m') 

which is close to zero but not quite equal.

UnitArrays are the array version of UnitScalars.::

   >>> from numpy import linspace
   >>> a = UnitArray(linspace(0, 5, 6), units="cm")
   >>> a
   UnitArray([ 0.,  1.,  2.,  3.,  4.,  5.], units='0.01*m')

UnitArrays can be multiplied by UnitScalars or other UnitArrays, as in NumPy.::

   >>> a * b
   UnitArray([0.,  1.,  2.,  3.,  4.,  5.], units='0.0030480000000000004*m**2')

Note that part of the value of the is contained in the unit string. To properly
deal with complicated units, we need to use :ref:`unitted functions
<unit-funcs>`.

.. _working-with-units-1:

Working with units (part 1)
===============================================================================
We can import units and use them outside of UnitScalars and UnitArrays,
too. This can be convenient not only as a desktop conversion tool but also for
use in :ref:`unitted functions <unit-funcs>`, as we'll see in the next
section.::

   >>> from scimath.units.length import foot, inch, meter
   >>> foot/inch
   12.0
   >>> foot/meter
   0.3048



.. _NumPy: http://www.numpy.org
.. _ndarray: http://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html
