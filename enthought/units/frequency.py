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
# Symbols defined: hz, khz
#
#------------------------------------------------------------------------------

#############################################################################
# Imports:
#############################################################################
from SI import hertz, kilo

#############################################################################
# Definitions:
#############################################################################

hertz.label = 'Hz'
kilohertz = kilo*hertz
kilohertz.label = 'kHz'

rpm = hertz/60

#############################################################################
# Aliases:
#############################################################################

hz = hertz
Hz = hertz
khz = kilohertz

#### EOF ######################################################################
