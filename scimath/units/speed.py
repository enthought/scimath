#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Travis N. Vaught
# Date: 05/22/2005
# Description: Define units of density
#
# Derived from: units/density.py [pyre system]
#               Michael A.G. Aivazis
#               California Institute of Technology
#               (c) 1998-2003
#
# Symbols defined: knot, feet_per_second, meters_per_second [and aliases]
#                  kilometers_per_second [and aliases]
#
#------------------------------------------------------------------------------

#############################################################################
# Imports:
#############################################################################

from __future__ import absolute_import
from .time import hour, minute, second, millisecond
from .length import foot, kilometer, meter, nautical_mile, mile
from .angle import radian, revolution

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
kilometers_per_hour = kilometer / hour
kilometers_per_hour.label = 'km/h'
miles_per_hour = mile / hour
miles_per_hour.label = 'mph'

# angular speeds
radiants_per_second = radiant / second
radiants_per_second.label = 'rad/s'
radiants_per_minute = radiant / minute
radiants_per_minute.label = 'rad/min'
revolutions_per_second = revolutions / second
revolutions_per_second.label = 'rev/s'
revolutions_per_minute = revolutions / minute
revolutions_per_minute.label = 'rev/min'
rpm = revolutions_per_minute

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

#### EOF ######################################################################
