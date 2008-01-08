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
# Description: Define units of acceleration
#
#  Symbols defined: feet_per_second_squared [and aliases]
#                   meters_per_second_squared [and aliases]
#
#------------------------------------------------------------------------------

#####################################################################
# Imports:
#####################################################################
from length import meter, foot
from time   import second

#####################################################################
# Definitions:
#####################################################################

feet_per_second_squared = foot/second**2
feet_per_second_squared.label = 'ft/s^2'
meters_per_second_squared = meter/second**2
meters_per_second_squared.label = 'm/s^2'

#####################################################################
# Aliases:
#####################################################################

ft_per_s2 = feet_per_second_squared
f_per_s2 = feet_per_second_squared
m_per_s2 = meters_per_second_squared

#### EOF ######################################################################
