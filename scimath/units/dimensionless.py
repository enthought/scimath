# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from copy import copy
from scimath.units.SI import dimensionless
from scimath.units.unit import one, dim

###############################################################################
# fractional or percentage units.
###############################################################################

fractional = copy(dimensionless)
fractional.label = 'V/V'
fraction = fractional
ratio = frac = fract = fractional

percent = fractional / 100.
percent.label = '%'
percentage = percent
pct = percent

###############################################################################
# concentration (parts per million)
###############################################################################

parts_per_one = copy(dimensionless)

parts_per_million = parts_per_one / 1e6
parts_per_million.label = 'ppm'
ppm = parts_per_million
