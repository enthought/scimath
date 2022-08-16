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

from .SI import joule, kilo, mega, giga


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
kilowatt_hour = 3.6e6 * joule

electron_volt = 1.60218e-19 * joule


# aliases

J = joule
kJ = kilo * joule
MJ = mega * joule

eV = electron_volt
KeV = kilo * eV
MeV = mega * eV
GeV = giga * eV

cal = calorie
kcal = kilo * calorie
