# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of density
Derived from: units/density.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""

#############################################################################
# Imports:
#############################################################################

from .mass import gram, kilogram, pound
from .volume import cubic_centimeter, cubic_meter, us_fluid_gallon
#############################################################################
# Definitions:
#############################################################################

grams_per_cubic_centimeter = gram / cubic_centimeter
grams_per_cubic_centimeter.label = 'g/cc'
kilograms_per_cubic_meter = kilogram / cubic_meter
kilograms_per_cubic_meter.label = 'kg/m3'
# Taken from geo_units pressure gradient section
# TODO: should this be here (density)?
lb_per_gal = pound / us_fluid_gallon
lb_per_gal.label = 'lb/gal'


#############################################################################
# Aliases:
#############################################################################

gcc = grams_per_cubic_centimeter
grams_per_cc = grams_per_cubic_centimeter
g_per_cc = grams_per_cubic_centimeter
gm_per_cc = grams_per_cubic_centimeter
g_per_c3 = grams_per_cubic_centimeter
gm_per_c3 = grams_per_cubic_centimeter
g_per_cm3 = grams_per_cubic_centimeter
gm_per_cm3 = grams_per_cubic_centimeter
kg_per_m3 = kilograms_per_cubic_meter
lb_per_gallon = lb_per_gal
