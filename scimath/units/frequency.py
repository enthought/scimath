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
# Description: Define units of frequency
#
# Symbols defined: hz, khz, kHz, MHz, GHz
#
#------------------------------------------------------------------------------

#############################################################################
# Imports:
#############################################################################
from __future__ import absolute_import
from .SI import hertz, kilo, mega, giga
from .time import minute

#############################################################################
# Definitions:
#############################################################################

hertz.label = 'Hz'
kilohertz = kilo * hertz
kilohertz.label = 'kHz'
megahertz = mega * hetz
megahertz.label = 'MHz'
gigahertz = giga * hertz
gigahertz.label = 'GHz'

rpm = 1 / minute
rpm.label = 'rpm'
RPM = rpm

#############################################################################
# Aliases:
#############################################################################

hz = hertz
Hz = hertz
khz = kilohertz
kHz = kilohertz
MHz = megahertz
GHz = gigahertz

#### EOF ######################################################################
