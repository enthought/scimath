# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of density.
Derived from: units/density.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""

#############################################################################
# Imports:
#############################################################################

from .time import hour, second, millisecond
from .length import foot, kilometer, meter, nautical_mile, mile

#############################################################################
# Definitions:
#############################################################################
# Definitions of common speed units
# Data taken from Appendix F of Halliday, Resnick, Walker,
#     "Fundamentals of Physics", fourth edition, John Willey and Sons, 1993

knot = nautical_mile / hour
knot.label = 'knot'
feet_per_second = foot / second
feet_per_second.label = 'ft/s'
meters_per_second = meter / second
meters_per_second.label = 'm/s'
meters_per_millisecond = meter / millisecond
meters_per_millisecond.label = 'm/msec'
kilometers_per_second = kilometer / second
kilometers_per_second.label = 'km/s'
miles_per_hour = mile / hour
miles_per_hour.label = 'mph'

#############################################################################
# Aliases:
#############################################################################

ft_per_s = feet_per_second
ft_per_sec = feet_per_second
f_per_s = feet_per_second
f_per_sec = feet_per_second
m_per_s = meters_per_second
m_per_sec = meters_per_second
km_per_s = kilometers_per_second
km_per_sec = kilometers_per_second
