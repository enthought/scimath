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
# Date: 08/2/2005
# Description: Define units of angle (dimensionless with meaning)
#
#
# Symbols defined: degree and variants
#
#------------------------------------------------------------------------------

#############################################################################
# Imports:
#############################################################################

import math
from SI import radian

#############################################################################
# Definitions:
#############################################################################

degree = radian * math.pi / 180.
degree.label = 'deg'
degrees = degree
deg = degree

radian.label = 'radians'
radians = radian