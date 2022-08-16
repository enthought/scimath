# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Define units of angle (dimensionless with meaning)
"""

#############################################################################
# Imports:
#############################################################################

import math
from .SI import radian

#############################################################################
# Definitions:
#############################################################################

degree = radian * math.pi / 180.
degree.label = 'deg'
degrees = degree
deg = degree

radian.label = 'rad'
radians = radian

grad = degree * 0.9
grad.label = '^g'
grads = grad
gon = grad
gons = grad

minute = degree / 60.0
minutes = minute
minute.label = "'"
second = degree / 3600.0
second.label = '"'
seconds = second

sign = degree * 30
signs = sign

revolution = 360 * degree
revolution.label = 'r'
revolutions = revolution
circle = revolution
circles = circle
turn = circle
turns = circles

quadrant = 90 * degree
quadrants = quadrant
right_angle = quadrant
right_angles = quadrant

sextant = 60 * degree
sextants = sextant

mil = 90 / 1600.0 * degree
mil.label = 'mil'
mils = mil
