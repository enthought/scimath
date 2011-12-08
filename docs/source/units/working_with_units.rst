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
sub-module are listed. Units are sometimes imported for convenience from the
module where they were defined. These cases are indicated in *italics*.


scimath.units.acceleration
--------------------------

f_per_s2, feet_per_second_squared, *foot*, ft_per_s2, m_per_s2,
*meter*, meters_per_second_squared, *second*

scimath.units.angle
-------------------

circle, circles, deg, degree, degrees, gon, gons, grad, grads, math, mil, mils, minute, minutes, quadrant, quadrants, radian, radians, revolution, revolutions, right_angle, right_angles, second, seconds, sextant, sextants, sign, signs, turn, turns

scimath.units.area
------------------

acre, barn, centimeter, foot, hectare, inch, meter, mile, square_centimeter, square_foot, square_inch, square_meter, square_mile

scimath.units.density
---------------------

cubic_centimeter, cubic_meter, g_per_c3, g_per_cc, g_per_cm3, gcc, gm_per_c3, gm_per_cc, gm_per_cm3, gram, grams_per_cc, grams_per_cubic_centimeter, kg_per_m3, kilogram, kilograms_per_cubic_meter, lb_per_gal, lb_per_gallon, pound, us_fluid_gallon

scimath.units.energy
--------------------

Btu, Calorie, GeV, J, KeV, MJ, MeV, cal, calorie, eV, electron_volt, erg, foot_pound, giga, horse_power_hour, joule, kJ, kcal, kilo, kilowatt_hour, mega

scimath.units.force
-------------------

lbf, newton

scimath.units.frequency
-----------------------

Hz, RPM, hertz, hz, khz, kilo, kilohertz, minute, rpm

scimath.units.geo_units
-----------------------

GPA, GPa, Gpa, MPA, MPa, MPa_per_100f, MPa_per_100ft, MPa_per_f, MPa_per_ft, MPa_per_m, Mpa, N, ampere, api, apsi, atto, bar, bars, becquerel, candela, centi, copy, coulomb, cubic_centimeter, cubic_foot, cubic_meter, deci, deka, dimensionless, exa, farad, femto, foot, frac, fraction, fractional, g_ft_per_cc_s, g_km_per_cc_s, gapi, giga, gpa, grams, gray, hecto, henry, hertz, inch, joule, katal, kbar, kbars, kilo, kilobar, kilogram, kilometers, lb, lb_per_gal, lb_per_gallon, lbf, lbs, liter, lumen, lux, m, mS, mSiemen, mega, meter, mho, micro, microsecond, milli, millivolts, mmho, mole, mpa, mv, nano, newton, none, ohm, ohm_m, ohm_meter, ohmm, ohms, ohms_per_m, ohms_per_meter, parts_per_million, parts_per_one, pascal, pct, percent, percentage, peta, pico, pounds_per_square_inch, ppg, ppm, psi, psi_per_f, psi_per_ft, psig, radian, ratio, second, siemen, siemens, siemens_per_m, siemens_per_meter, sievert, steradian, tera, tesla, unit, us_fluid_gallon, us_per_ft, v, volt, volts, watt, weber, yocto, yotta, zepto, zetta

scimath.units.length
--------------------

IN, angstrom, astronomical_unit, centi, centimeter, centimeters, cm, f, fathom, feet, fermi, foot, ft, inch, inches, kilo, kilometer, kilometers, km, light_year, m, meter, meters, micro, micrometer, micron, mile, milli, millimeter, millimeters, mm, nano, nanometer, nautical_mile, nm, parsec, um, yard

scimath.units.mass
------------------

centi, centigram, cg, g, gm, gram, grams, kg, kilo, kilogram, kilograms, lb, lbs, metric_ton, mg, milli, milligram, ounce, pound, pounds, ton

scimath.units.power
-------------------

horsepower, kilo, kilowatt, kw, watt

scimath.units.pressure
----------------------

GPa, MPa, Pa, atm, atmosphere, bar, giga, kPa, kilo, mega, millibar, pascal, torr

scimath.units.SI
----------------

ampere, atto, becquerel, candela, centi, copy, coulomb, deci, deka, dimensionless, exa, farad, femto, giga, gray, hecto, henry, hertz, joule, katal, kilo, kilogram, lumen, lux, mega, meter, micro, milli, mole, nano, newton, none, ohm, pascal, peta, pico, radian, second, siemens, sievert, steradian, tera, tesla, unit, volt, watt, weber, yocto, yotta, zepto, zetta

scimath.units.speed
-------------------

f_per_s, f_per_sec, feet_per_second, foot, ft_per_s, ft_per_sec, hour, kilometer, kilometers_per_second, km_per_s, km_per_sec, knot, m_per_s, m_per_sec, meter, meters_per_millisecond, meters_per_second, mile, miles_per_hour, millisecond, nautical_mile, second

scimath.units.substance
-----------------------

kilo, kmol, mol, mole

scimath.units.temperature
-------------------------

K, celsius, degC, degF, degK, degc, degf, degk, fahrenheit, kelvin, rankine

scimath.units.time
------------------

day, hour, micro, microsecond, microseconds, milli, millisecond, milliseconds, minute, ms, msec, nano, nanosecond, ns, pico, picosecond, ps, s, sec, second, seconds, us, usec, year

scimath.units.volume
--------------------

V, barrel, bbl, c3, cc, centimeter, cm3, cubic_centimeter, cubic_foot, cubic_inch, cubic_meter, cuft, f3, foot, ft3, gallon, gallons, inch, liter, liters, m3, meter, us_fluid_gallon, us_fluid_ounce, us_fluid_quart, us_pint

