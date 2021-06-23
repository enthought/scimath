.. _extend-unit-parser:

===============================================================================
Extending the Unit Parser
===============================================================================

If you define a series of units that you want to be available for import and
use in unitted functions, then you must use the unit_parser as below::

    from scimath.units.api import unit_parser
    from scimath.units.mass import kilogram

    apple = 0.2 * kilogram
    apple.label = 'label'

    bread = 0.5 * kilogram
    bread.label = 'loaf of bread'

    very_small_rocks = 0.02 * kilogram
    very_small_rocks.label = 'very small rocks'

    a_duck = 1.3 * kilogram
    a_duck.label = 'a duck'

    unit_parser.parser.extend(u)

When the above module is imported, ``unit_parser`` will be updated, and a
unitted function can be built, as follows::

    from scimath.units.api import has_units

    @has_units
    def witch_test(mass_of_maiden):
         """ Test to determine if one or more young maidens is a witch.

	 Parameters
	 ----------
     	 mass_of_maiden : array : units=a_duck
             array of masses to check against the weight of a duck

     	 Returns
     	 -------
     	 truth : bool
         """ 
     	 return mass_of_maiden >= 1

The behavior is as expected:
 >>> from scimath.units.mass import pound
 >>> from scimath.units.api import UnitArray
 >>> from numpy.random import randn
 >>> maidens = UnitArray(randn(5)*15 + 100, units="pound")
 >>> witch_test(maidens)
 array([ True,  True,  True,  True,  True], dtype=bool)
