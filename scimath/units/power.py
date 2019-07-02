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
from .SI import watt, kilo, mega, giga, tera, milli

#
# Definitions of common power units
# Data taken from Appendix F of Halliday, Resnick, Walker, "Fundamentals of Physics",
#     fourth edition, John Willey and Sons, 1993

milliwatt = milli * watt
milliwatt.label = 'mW'
kilowatt = kilo * watt
kilowatt.label = 'kW'
megawatt = mega * watt
megawatt.label = 'MW'
gigawatt = giga * watt
gigawatt.label = 'GW'
terawatt = tera * watt
terawatt.label = 'TW'
horsepower = 745.7 * watt

# aliases

mW = milliwatt
W = watt
kW = kilowatt
MW = megawatt
GW = gigawatt
TW = terawatt


# version
__id__ = "$Id: power.py,v 1.1.1.1 2003/07/02 21:39:14 aivazis Exp $"

#
# End of file
