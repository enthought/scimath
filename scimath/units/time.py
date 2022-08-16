# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of time
Derived from: units/time.py [pyre system]
              Michael A.G. Aivazis
              California Institute of Technology
              (c) 1998-2003
"""

#############################################################################
# Imports:
#############################################################################

from .SI import second
from .SI import pico, nano, micro, milli

#############################################################################
# Definitions:
#############################################################################
# Definitions of common time units
# Data taken from Appendix F of Halliday, Resnick, Walker,
#     "Fundamentals of Physics", fourth edition, John Willey and Sons, 1993

second.label = 'second'
picosecond = pico * second
picosecond.label = 'picosecond'
nanosecond = nano * second
nanosecond.label = 'nanosecond'
microsecond = micro * second
microsecond.label = 'microsecond'
millisecond = milli * second
millisecond.label = 'millisecond'

# other common units

minute = 60 * second
minute.label = "minute"
hour = 60 * minute
hour.label = "hour"
day = 24 * hour
day.label = "day"
week = 7 * day
week.label = "week"
year = 365.25 * day
year.label = "year"

#############################################################################
# Aliases:
#############################################################################

s = sec = second
ps = picosecond
ns = nanosecond
us = usec = microsecond
ms = msec = millisecond

# plural aliases
seconds = second
microseconds = microsecond
milliseconds = millisecond

minutes = minute
hours = hour
days = day
weeks = week
years = year
