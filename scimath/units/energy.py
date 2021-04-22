#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2003  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from __future__ import absolute_import
from .SI import joule, kilo, mega, giga, tera, milli


#
# Definitions of common energy units
#
# Data taken from
#
#     Appendix F of Halliday, Resnick, Walker, "Fundamentals of Physics",
#         fourth edition, John Willey and Sons, 1993
#
#     The NIST Reference on Constants, Units and Uncertainty,
#         http://physics.nist.gov/cuu
#


Btu = 1055 * joule
erg = 1e-7 * joule
foot_pound = 1.356 * joule
horse_power_hour = 2.685e6 * joule

calorie = 4.1858 * joule
Calorie = 1000 * calorie
watt_hour = 3.6e3 * joule

electron_volt = 1.60218e-19 * joule


# aliases

J = joule
millijoule = milli * joule
kilojoule = kilo * joule
megajoule = mega * joule
gigajoule = giga * joule
terajoule = tera * joule

mJ = millijoule
kJ = kilojoule
MJ = megajoule
GJ = gigajoule
TJ = terajoule

eV = electron_volt
KeV = kilo * eV
MeV = mega * eV
GeV = giga * eV

cal = calorie
kilocalorie = kilo * calorie
kcal = kilocalorie

watt_second = joule
kilowatt_hour = kilo * watt_hour
megawatt_hour = mega * watt_hour
gigawatt_hour = giga * watt_hour
terawatt_hour = tera * watt_hour

Ws = watt_second
Wh = watt_hour
kWh = kilowatt_hour
MWh = megawatt_hour
GWh = gigawatt_hour
TWh = terawatt_hour


# version
__id__ = "$Id: energy.py,v 1.1.1.1 2003/07/02 21:39:14 aivazis Exp $"

#
# End of file
