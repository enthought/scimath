#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2003  All Rights Reserved
#
# <LicenseText>
#
# Modified: 2005-05-23, Travis N. Vaught added label attribs and more aliases
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from scimath.units.unit import unit

# Tk = Tk
# Tk = 1 * (Tc+273.15)
# Tk = 5/9 * (Tr)
# Tk = 5/9 * (Tf + 459.67)

kelvin = unit(1.0, (0, 0, 0, 0, 1, 0, 0), 0.0)
kelvin.label = 'kelvin'
celsius = unit(1.0, (0, 0, 0, 0, 1, 0, 0), 273.15)
celsius.label = 'celsius'
rankine = unit(5.0 / 9.0, (0, 0, 0, 0, 1, 0, 0), 0.0)
fahrenheit = unit(5.0 / 9.0, (0, 0, 0, 0, 1, 0, 0), 459.67)
fahrenheit.label = 'fahrenheit'

# aliases
K = kelvin
degC = celsius
degc = celsius
degF = fahrenheit
degf = fahrenheit
degK = kelvin
degk = kelvin

# version
__id__ = "$Id: temperature.py,v 1.1.1.1 2003/07/02 21:39:14 aivazis Exp $"

#
# End of file
