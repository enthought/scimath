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
