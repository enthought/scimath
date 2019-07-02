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
from copy import copy

from .SI import newton, milli, kilo, mega

N = newton
millinewton = milli * newton
kilonewton = kilo * newton
meganewton = mega * newton

mN = millinewton
kN = kilonewton
MN = meganewton

lbf = 4.44822 * newton
lbf.label = 'lbf'
lbs = lbf
