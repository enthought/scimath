.. _working-with-units:

===============================================================================
Working With Units
===============================================================================

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

For example, the predefined unit Newton has the following attributes::

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

Conversions can be made between units with the same derivation::

 >>> from scimath.units.api import convert
 >>> convert(1, lbf, newton)
 4.44822


Types of Units Available
===============================================================================
In the following sections, the units available from each scimath.units
sub-module are listed. For convenience units are sometimes imported into a
module from the module where they were defined.


scimath.units.acceleration
--------------------------

f_per_s2, feet_per_second_squared, ft_per_s2, m_per_s2,
meters_per_second_squared

scimath.units.angle
-------------------

circle, circles, deg, degree, degrees, gon, gons, grad, grads, math, mil, mils, minute, minutes, quadrant, quadrants, radian, radians, revolution, revolutions, right_angle, right_angles, second, seconds, sextant, sextants, sign, signs, turn, turns

scimath.units.area
------------------

acre, barn, hectare, square_centimeter, square_foot, square_inch, square_meter, square_mile

scimath.units.density
---------------------

g_per_c3, g_per_cc, g_per_cm3, gcc, gm_per_c3, gm_per_cc, gm_per_cm3,
grams_per_cc, grams_per_cubic_centimeter, kg_per_m3, kilograms_per_cubic_meter,
lb_per_gal, lb_per_gallon

scimath.units.energy
--------------------

Btu, Calorie, GeV, J, KeV, MJ, MeV, cal, calorie, eV, electron_volt, erg, foot_pound, horse_power_hour, joule, kJ, kcal, kilowatt_hour

scimath.units.force
-------------------

lbf, newton

scimath.units.frequency
-----------------------

Hz, RPM, hertz, hz, khz, kilohertz, rpm

scimath.units.geo_units
-----------------------

GPA, GPa, Gpa, MPA, MPa, MPa_per_100f, MPa_per_100ft, MPa_per_f, MPa_per_ft, MPa_per_m, Mpa, api, apsi, becquerel, candela, coulomb, cubic_foot, cubic_meter, farad, foot, frac, fraction, fractional, g_ft_per_cc_s, g_km_per_cc_s, gapi, gpa, grams, gray, henry, hertz, inch, joule, katal, kilogram, kilometers, lb, lb_per_gal, lb_per_gallon, lbf, lbs, liter, lumen, lux, m, mS, mSiemen, meter, mho, microsecond, millivolts, mmho, mole, mpa, mv, nano, newton, ohm, ohm_m, ohm_meter, ohmm, ohms, ohms_per_m, ohms_per_meter, parts_per_million, parts_per_one, pascal, pct, percent, percentage, pico, ppg, ppm, psi_per_f, psi_per_ft, radian, ratio, second, siemen, siemens, siemens_per_m, siemens_per_meter, sievert, steradian, tesla, us_fluid_gallon, us_per_ft, v, volt, volts, watt, weber

scimath.units.length
--------------------

IN, angstrom, astronomical_unit, centimeter, centimeters, cm, f, fathom, feet,
fermi, foot, ft, inch, inches, kilometer, kilometers, km, light_year, m, meter,
meters, micrometer, micron, mile, millimeter, millimeters, mm, nanometer,
nautical_mile, nm, parsec, um, yard

scimath.units.mass
------------------

centigram, cg, g, gm, gram, grams, kg, kilogram, kilograms, lb, lbs,
metric_ton, mg, milligram, ounce, pound, pounds, ton

scimath.units.power
-------------------

horsepower, kilowatt, kw, watt

scimath.units.pressure
----------------------

GPa, MPa, Pa, apsi,  atm, atmosphere, bar, kPa, kbar, kbars, kilobar, millibar,
pascal, punds_per_square_inch, psi, psig, torr

scimath.units.SI
----------------

ampere, atto, becquerel, candela, centi, copy, coulomb, deci, deka,
dimensionless, exa, farad, femto, giga, gray, hecto, henry, hertz, joule,
katal, kilo, kilogram, lumen, lux, mega, meter, micro, milli, mole, nano,
newton, none, ohm, pascal, peta, pico, radian, second, siemens, sievert,
steradian, tera, tesla, unit, volt, watt, weber, yocto, yotta, zepto, zetta

scimath.units.speed
-------------------

f_per_s, f_per_sec, feet_per_second, ft_per_s, ft_per_sec,
kilometers_per_second, km_per_s, km_per_sec, knot, m_per_s, m_per_sec,
meters_per_millisecond, meters_per_second, miles_per_hour

scimath.units.substance
-----------------------

kmol, mol, mole

scimath.units.temperature
-------------------------

K, celsius, degC, degF, degK, degc, degf, degk, fahrenheit, kelvin, rankine

scimath.units.time
------------------

day, hour, micro, microsecond, microseconds, milli, millisecond, milliseconds,
minute, ms, msec, nano, nanosecond, ns, pico, picosecond, ps, s, sec, second,
seconds, us, usec, year

scimath.units.volume
--------------------

barrel, bbl, c3, cc, centimeter, cm3, cubic_centimeter, cubic_foot, cubic_inch,
cubic_meter, cuft, f3, ft3, gallon, gallons, liter, liters, m3,
us_fluid_gallon, us_fluid_ounce, us_fluid_quart, us_pint

