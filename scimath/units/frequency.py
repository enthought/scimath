# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Defines units of frequency
"""

#############################################################################
# Imports:
#############################################################################
from .SI import hertz, kilo
from .time import minute

#############################################################################
# Definitions:
#############################################################################

hertz.label = 'Hz'
kilohertz = kilo * hertz
kilohertz.label = 'kHz'

rpm = 1 / minute
rpm.label = 'rpm'
RPM = rpm

#############################################################################
# Aliases:
#############################################################################

hz = hertz
Hz = hertz
khz = kilohertz
