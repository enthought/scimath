# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2003  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from copy import copy
from scimath.units.unit import unit, dimensionless, none

# basic SI units

meter = unit(1.0, (1, 0, 0, 0, 0, 0, 0))
kilogram = unit(1.0, (0, 1, 0, 0, 0, 0, 0))
second = unit(1.0, (0, 0, 1, 0, 0, 0, 0))
ampere = unit(1.0, (0, 0, 0, 1, 0, 0, 0))
mole = unit(1.0, (0, 0, 0, 0, 0, 1, 0))
candela = unit(1.0, (0, 0, 0, 0, 0, 0, 1))
# moved kelvin to temperature for now

# the 22 derived SI units with special names

radian = copy(dimensionless)  # plane angle
radian.label = 'radian'

steradian = copy(dimensionless)  # solid angle
steradian.label = 'steradian'
hertz = 1 / second  # frequency
hertz.label = 'Hz'
newton = meter * kilogram / second**2  # force
newton.label = 'newton'

pascal = newton / meter**2  # pressure
pascal.label = 'pascal'

joule = newton * meter  # work, heat
joule.label = 'joule'

watt = joule / second  # power, radiant flux
watt.label = 'watt'
coulomb = ampere * second  # electric charge
coulomb.label = 'coulomb'

volt = watt / ampere  # electric potential difference
volt.label = 'volt'

farad = coulomb / volt  # capacitance
farad.label = 'farad'

ohm = volt / ampere  # electric resistance
ohm.label = 'ohm'

siemens = ampere / volt  # electric conductance
siemens.label = 'siemens'

weber = volt * second  # magnetic flux
weber.label = 'weber'

tesla = weber / meter**2  # magnetic flux density
tesla.label = 'tesla'

henry = weber / ampere  # inductance
henry.label = 'henry'

lumen = candela * steradian  # luminus flux
lumen.label = 'lumen'

lux = lumen / meter**2  # illuminance
lux.label = 'lux'

becquerel = 1 / second  # radioactivity
becquerel.label = 'becquerel'

gray = joule / kilogram  # absorbed dose
gray.label = 'gray'

sievert = joule / kilogram  # dose equivalent
sievert.label = 'sievert'

katal = mole / second  # catalytic activity
katal.label = 'katal'

# prefixes

yotta = 1e24
zetta = 1e21
exa = 1e18
peta = 1e15
tera = 1e12
giga = 1e9
mega = 1e6
kilo = 1000
hecto = 100
deka = 10
deci = .1
centi = .01
milli = .001
micro = 1e-6
nano = 1e-9
pico = 1e-12
femto = 1e-15
atto = 1e-18
zepto = 1e-21
yocto = 1e-24
