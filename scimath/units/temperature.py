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
