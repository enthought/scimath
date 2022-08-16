# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of length
Derived from: units/length.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""

#############################################################################
# Imports:
#############################################################################


from .SI import meter
from .SI import kilo, centi, milli, micro, nano

#############################################################################
# Definitions:
#############################################################################
# Definitions of common length units
# Data taken from Appendix F of Halliday, Resnick, Walker,
#     "Fundamentals of Physics", fourth edition, John Willey and Sons, 1993

meter.label = 'meter'
nanometer = nano * meter
nanometer.label = 'nanometer'
micrometer = micro * meter
micrometer.label = 'micrometer'
millimeter = milli * meter
millimeter.label = 'millimeter'
centimeter = centi * meter
centimeter.label = 'centimeter'
kilometer = kilo * meter
kilometer.label = 'kilometer'

# British units
inch = 2.540 * centimeter
inch.label = 'inch'
foot = 12 * inch
foot.label = 'feet'
yard = 3 * foot
mile = 5280 * foot

fathom = 6 * foot
nautical_mile = 1852 * meter

# others
angstrom = 1e-10 * meter
fermi = 1e-15 * meter
survey_foot = 1200.0 / 3937.0 * meter
survey_foot.label = 'us_foot'
us_foot = survey_foot
us_feet = survey_foot

astronomical_unit = 1.49598e11 * meter
light_year = 9.460e12 * kilometer
parsec = 3.084e13 * kilometer

#############################################################################
# Aliases:
#############################################################################

m = meter
nm = nanometer
um = micrometer
micron = micrometer
mm = millimeter
cm = centimeter
km = kilometer

f = foot
ft = foot
feet = foot

millimeters = millimeter
centimeters = centimeter

meters = meter
kilometers = kilometer
inches = IN = inch
