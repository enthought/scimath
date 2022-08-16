# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of mass
Derived from: units/mass.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""

#############################################################################
# Imports:
#############################################################################

from .SI import kilogram
from .SI import kilo, centi, milli

#############################################################################
# Definitions:
#############################################################################
# Definitions of common mass units
# Data taken from Appendix F of Halliday, Resnick, Walker, "Fundamentals of Physics",
#     fourth edition, John Willey and Sons, 1993

kilogram.label = 'kilogram'
gram = kilogram / kilo
gram.label = 'gram'
centigram = centi * gram
centigram.label = 'centigram'
milligram = milli * gram
milligram.label = 'milligram'

metric_ton = 1000 * kilogram

ounce = 28.35 * gram
ounce.label = 'ounce'
pound = 16 * ounce
pound.label = 'pound'
ton = 2000 * pound
ton.label = 'ton'

#############################################################################
# Aliases:
#############################################################################

kilograms = kilogram

kg = kilogram
g = gram
cg = centigram
mg = milligram
grams = gram
gm = gram
lb = pound
pounds = pound
lbs = lb
