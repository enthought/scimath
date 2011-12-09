===============================================================================
Introduction to SciMath Units
===============================================================================

A large number of units used in science and engineering are available for use,
and scimath.units makes working with and converting among them easy.


Getting Started
===============================================================================
We can import units from the scimath.units submodules. (See :ref:`list of
available units <available-units>` for a listing by submodule.) There are
submodules for many categories of physical quantities.

 >>> from scimath.units.length import foot, inch, meter
 >>> foot / inch
 12.0
 >>> foot / meter
 0.3048

.. _conversion-factor-caveat:

**Caution**: If you are using this tool to produce conversion factors, remember
that the factor is the *inverse* of what it looks like. Above, we divided one
foot by one meter to get the ratio 0.3048. That is, ``foot / meter`` yields the
number of meters per foot. Be careful to think through the logic clearly when
developing conversion factors.

You can define your own arbitrary units and use them for calculating conversion
factors::

 >>> from scimath.units.length import inch
 >>> from scimath.units.force import lbf
 >>> from scimath.units.pressure import torr
 >>> my_psi = 2 * lbf / inch ** 2
 >>> my_psi / torr
 103.44718363855331

Internally, they are stored as a combination of fundamental physical
quantities expressed in the SI system

 >>> my_psi
 13789.509579019157*m**-1*kg*s**-2

Conversions can be made between units with the same derivation using :py:func:`~scimath.units.convert.convert`:

 >>> from scimath.units.api import convert
 >>> from scimath.units.force import lbf, newton
 >>> convert(1, lbf, newton)
 4.44822

However, adding incompatible units raises an ``IncompatibleUnits`` exception:

 >>> from scimath.units.electromagnetism import volt
 >>> from scimath.units.mass import kilogram
 >>> 1 * volt + 2 * kilogram
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
   File "scimath/units/unit.py", line 62, in __add__
     raise IncompatibleUnits("add", self, other)
 scimath.units.unit.IncompatibleUnits: Cannot add quanitites with units of 'm**2*kg*s**-3*A**-1' and 'kg'


