from copy import copy

from scimath.units.SI import *
from scimath.units.dimensionless import fractional, fraction, frac, \
     percent, percentage, pct, parts_per_one, parts_per_million, ppm, ratio
from scimath.units.electromagnetism import mho, millivolts, mmho, mSiemen, \
     mS, mv, ohms, ohmm, ohm_m, ohm_meter, ohms_per_m, ohms_per_meter, \
     siemen, siemens_per_meter, siemens_per_m, volts, v
from scimath.units.force import lbf, lbs, N
from scimath.units.length import foot, inch, m, meter, kilometers
from scimath.units.mass import grams, lb
from scimath.units.pressure import apsi, bar, bars, gpa, Gpa, GPA, GPa, kbar, \
     kbars, kilobar, mpa, Mpa, MPA, MPa, pounds_per_square_inch, psi, psig
from scimath.units.time import microsecond
from scimath.units.volume import cubic_centimeter, cubic_meter, \
     us_fluid_gallon, liter, cubic_foot
     

###############################################################################
# impedance_units          g*km/cc/s, g*f/cc/s
###############################################################################
g_km_per_cc_s = (grams*kilometers)/(cubic_centimeter*second)
g_km_per_cc_s.label = 'g*km/(cc*s)'
g_ft_per_cc_s = (grams*foot)/(cubic_centimeter*second)
g_ft_per_cc_s.label = 'g*ft/(cc*s)'

###############################################################################
# modulus_units            GPa, MPa
# pressure_units           MPa, psi, kbar, bar
# imported from scimath.units.pressure
###############################################################################



###############################################################################
# pressure_gradient_units  psi/f, MPa/m, lb/gal, MPa/100f
###############################################################################

psi_per_f  = psi/foot
psi_per_f.label  = 'psi/ft'
psi_per_ft = psi_per_f

MPa_per_m = MPa/meter
MPa_per_m.label = 'MPa/m'

lb_per_gal    = lb/us_fluid_gallon
lb_per_gallon = lb_per_gal

###############################################################################
# PPG seems to have units of mass/volume and not weight/volume so we cannot
# use the unit system to automatically convert for us unless we lie about
# the dimensionality of ppg and pretend it is the same as psi/ft.
###############################################################################
# This is dimensionally inconsistant which may bite us later.
###############################################################################

psi_per_ft = pounds_per_square_inch /foot
ppg        = psi_per_ft / 0.0519

MPa_per_f  = MPa/foot
MPa_per_f.label = 'MPa/ft'
MPa_per_ft = MPa_per_f
MPa_per_100f  = MPa/(100*foot)
MPa_per_100f.label = 'MPa/100ft'
MPa_per_100ft = MPa_per_100f


###############################################################################
# Gamma Ray
###############################################################################
api = copy(dimensionless)
gapi = copy(dimensionless)

###############################################################################
# psonic
###############################################################################
us_per_ft = microsecond/foot
us_per_ft = 'us/ft'