.. _user-ref:

===============================================================================
SciMath Units User Reference
===============================================================================

.. _internal-representation:

Internal Representation
===============================================================================

Internally, a scimath unit is a unit object:

.. py:class:: unit(value, derivation)

   .. py:attribute:: value

      a scalar quantity which holds the magnitude of the unit, relative to the
      derivation in SI units.

   .. py:attribute:: derivation

      a 7-tuple holding the power of each fundamental quantity in the unit:
      (length, mass, time, electrical current, temperature, amount of
      substance, luminous intensity). The labels of the fundamental quantities
      are given in the attribute _labels=('m', 'kg', 's', 'A', 'K', 'mol',
      'cd')

   .. py:attribute:: label

      the display name of the unit.

For example, the predefined unit Newton has the following attributes:

 >>> from scimath.units.force import newton, lbf
 >>> newton.value
 1.0
 >>> newton.derivation
 (1, 1, -2, 0, 0, 0, 0)
 >>> newton.label
 'newton'
 >>> lbf.value
 4.44822
 >>> lbf.derivation
 (1, 1, -2, 0, 0, 0, 0)

Limited API reference
===============================================================================

Convert
-------------------------------------------------------------------------------
.. autofunction:: scimath.units.convert.convert

HasUnits
-------------------------------------------------------------------------------
.. autofunction:: scimath.units.has_units.has_units

UnitScalar
-------------------------------------------------------------------------------
.. autofunction:: scimath.units.unit_scalar.UnitScalar

UnitArray
-------------------------------------------------------------------------------
.. autofunction:: scimath.units.unit_scalar.UnitArray
