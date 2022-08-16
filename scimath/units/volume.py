# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Description: Define units of volume

Derived from: units/volume.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""
#############################################################################
# Imports:
#############################################################################

from .length import meter, centimeter, foot, inch

#############################################################################
# Definitions:
#############################################################################
#
# Definitions of common volume units
# Data taken from Appendix F of Halliday, Resnick, Walker, "Fundamentals of Physics",
#     fourth edition, John Willey and Sons, 1993

cubic_meter = meter**3
cubic_meter.label = 'cubic meters'
cubic_centimeter = centimeter**3
cubic_centimeter.label = 'cubic centimeters'
cubic_foot = foot**3
cubic_foot.label = 'cubic feet'
cubic_inch = inch**3
cubic_inch.label = 'cubic_inches'

liter = 1000 * cubic_centimeter
liter.label = 'liters'

barrel = 5.61458 * cubic_foot
barrel.label = 'barrel'

us_fluid_ounce = 231. / 128. * cubic_inch
us_pint = 16 * us_fluid_ounce
us_fluid_quart = 2 * us_pint
us_fluid_gallon = 4 * us_fluid_quart

#############################################################################
# Aliases:
#############################################################################

c3 = cubic_centimeter
cm3 = cubic_centimeter
cc = cm3

m3 = V = cubic_meter

f3 = cubic_foot
ft3 = f3
cuft = f3

liters = liter

bbl = barrel

gallon = gallons = us_fluid_gallon
